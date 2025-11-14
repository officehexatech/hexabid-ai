import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, Like, Between, In } from 'typeorm';
import { Tender } from '../../database/entities/tender.entity';
import { CreateTenderDto } from './dto/create-tender.dto';
import { UpdateTenderDto } from './dto/update-tender.dto';
import { SearchTendersDto } from './dto/search-tenders.dto';
import { PaginatedResult } from '../../common/interfaces/paginated-result.interface';

@Injectable()
export class TenderService {
  constructor(
    @InjectRepository(Tender)
    private tenderRepository: Repository<Tender>,
  ) {}

  async findAll(
    query: SearchTendersDto,
    tenantId: string,
  ): Promise<PaginatedResult<Tender>> {
    const {
      page = 1,
      limit = 20,
      search,
      status,
      category,
      minValue,
      maxValue,
      region,
      source,
      sortBy = 'createdAt',
      sortOrder = 'DESC',
    } = query;

    const skip = (page - 1) * limit;

    const where: any = { deletedAt: null };

    if (search) {
      where.title = Like(`%${search}%`);
    }

    if (status) {
      where.status = status;
    }

    if (category) {
      where.category = category;
    }

    if (region) {
      where.region = region;
    }

    if (source) {
      where.source = source;
    }

    if (minValue || maxValue) {
      where.tenderValue = Between(
        minValue || 0,
        maxValue || 999999999,
      );
    }

    const [data, total] = await this.tenderRepository.findAndCount({
      where,
      take: limit,
      skip,
      order: { [sortBy]: sortOrder },
      relations: ['assignedUser'],
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

  async findOne(id: string, tenantId: string): Promise<Tender> {
    const tender = await this.tenderRepository.findOne({
      where: { id, deletedAt: null },
      relations: ['assignedUser'],
    });

    if (!tender) {
      throw new NotFoundException('Tender not found');
    }

    return tender;
  }

  async create(
    dto: CreateTenderDto,
    userId: string,
    tenantId: string,
  ): Promise<Tender> {
    const tender = this.tenderRepository.create({
      ...dto,
      createdBy: userId,
      status: 'discovered',
      parsingStatus: 'pending',
    });

    return this.tenderRepository.save(tender);
  }

  async update(
    id: string,
    dto: UpdateTenderDto,
    tenantId: string,
  ): Promise<Tender> {
    const tender = await this.findOne(id, tenantId);

    Object.assign(tender, dto);

    return this.tenderRepository.save(tender);
  }

  async remove(id: string, tenantId: string): Promise<void> {
    const tender = await this.findOne(id, tenantId);
    tender.deletedAt = new Date();
    await this.tenderRepository.save(tender);
  }
}
