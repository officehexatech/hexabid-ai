import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, Like } from 'typeorm';
import { OEMVendor } from '../../database/entities/oem-vendor.entity';
import { VendorQuote } from '../../database/entities/vendor-quote.entity';
import { CreateOEMVendorDto } from './dto/create-oem-vendor.dto';
import { UpdateOEMVendorDto } from './dto/update-oem-vendor.dto';
import { SearchVendorsDto } from './dto/search-vendors.dto';
import { PaginatedResult } from '../../common/interfaces/paginated-result.interface';

@Injectable()
export class OEMService {
  constructor(
    @InjectRepository(OEMVendor)
    private oemVendorRepository: Repository<OEMVendor>,
    @InjectRepository(VendorQuote)
    private vendorQuoteRepository: Repository<VendorQuote>,
  ) {}

  async findAll(
    query: SearchVendorsDto,
    tenantId: string,
  ): Promise<PaginatedResult<OEMVendor>> {
    const { page = 1, limit = 20, search, category, isActive = true } = query;
    const skip = (page - 1) * limit;

    const where: any = { isActive };

    if (search) {
      where.companyName = Like(`%${search}%`);
    }

    const [data, total] = await this.oemVendorRepository.findAndCount({
      where,
      take: limit,
      skip,
      order: { companyName: 'ASC' },
    });

    return {
      data,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  async findOne(id: string, tenantId: string): Promise<OEMVendor> {
    const vendor = await this.oemVendorRepository.findOne({
      where: { id, isActive: true },
    });

    if (!vendor) {
      throw new NotFoundException('Vendor not found');
    }

    return vendor;
  }

  async create(
    dto: CreateOEMVendorDto,
    tenantId: string,
  ): Promise<OEMVendor> {
    const vendor = this.oemVendorRepository.create(dto);
    return this.oemVendorRepository.save(vendor);
  }

  async update(
    id: string,
    dto: UpdateOEMVendorDto,
    tenantId: string,
  ): Promise<OEMVendor> {
    const vendor = await this.findOne(id, tenantId);
    Object.assign(vendor, dto);
    return this.oemVendorRepository.save(vendor);
  }

  async remove(id: string, tenantId: string): Promise<void> {
    const vendor = await this.findOne(id, tenantId);
    vendor.isActive = false;
    await this.oemVendorRepository.save(vendor);
  }

  async getVendorQuotes(vendorId: string, tenantId: string) {
    const quotes = await this.vendorQuoteRepository.find({
      where: { vendorId },
      relations: ['tender'],
      order: { createdAt: 'DESC' },
      take: 20,
    });

    return quotes;
  }
}
