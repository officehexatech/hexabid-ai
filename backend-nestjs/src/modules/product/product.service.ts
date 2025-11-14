import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, Like } from 'typeorm';
import { Product } from '../../database/entities/product.entity';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { SearchProductsDto } from './dto/search-products.dto';
import { PaginatedResult } from '../../common/interfaces/paginated-result.interface';

@Injectable()
export class ProductService {
  constructor(
    @InjectRepository(Product)
    private productRepository: Repository<Product>,
  ) {}

  async findAll(
    query: SearchProductsDto,
    tenantId: string,
  ): Promise<PaginatedResult<Product>> {
    const { page = 1, limit = 20, search, category, oemId } = query;
    const skip = (page - 1) * limit;

    const where: any = { isActive: true };

    if (search) {
      where.productName = Like(`%${search}%`);
    }

    if (category) {
      where.category = category;
    }

    if (oemId) {
      where.oemVendorId = oemId;
    }

    const [data, total] = await this.productRepository.findAndCount({
      where,
      take: limit,
      skip,
      relations: ['oemVendor'],
      order: { createdAt: 'DESC' },
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

  async findOne(id: string, tenantId: string): Promise<Product> {
    const product = await this.productRepository.findOne({
      where: { id, isActive: true },
      relations: ['oemVendor'],
    });

    if (!product) {
      throw new NotFoundException('Product not found');
    }

    return product;
  }

  async create(dto: CreateProductDto, tenantId: string): Promise<Product> {
    const product = this.productRepository.create(dto);
    return this.productRepository.save(product);
  }

  async update(
    id: string,
    dto: UpdateProductDto,
    tenantId: string,
  ): Promise<Product> {
    const product = await this.findOne(id, tenantId);
    Object.assign(product, dto);
    return this.productRepository.save(product);
  }

  async remove(id: string, tenantId: string): Promise<void> {
    const product = await this.findOne(id, tenantId);
    product.isActive = false;
    await this.productRepository.save(product);
  }

  async findMatches(
    dto: { description: string; specifications?: string },
    tenantId: string,
  ) {
    // Simple keyword matching (in production, use vector similarity)
    const keywords = dto.description.toLowerCase().split(' ');

    const products = await this.productRepository
      .createQueryBuilder('product')
      .where('product.isActive = :isActive', { isActive: true })
      .andWhere(
        `(
        LOWER(product.productName) LIKE :search OR
        LOWER(product.technicalDescription) LIKE :search
      )`,
        { search: `%${keywords[0]}%` },
      )
      .limit(10)
      .getMany();

    return {
      matches: products.map((product) => ({
        product,
        confidence: 0.75, // Mock confidence score
        matchingAttributes: ['name', 'description'],
      })),
    };
  }
}
