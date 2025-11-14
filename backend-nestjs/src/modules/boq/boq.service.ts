import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { BOQItem } from '../../database/entities/boq-item.entity';
import { Tender } from '../../database/entities/tender.entity';
import { CreateBOQItemDto } from './dto/create-boq-item.dto';
import { UpdateBOQItemDto } from './dto/update-boq-item.dto';

@Injectable()
export class BOQService {
  constructor(
    @InjectRepository(BOQItem)
    private boqItemRepository: Repository<BOQItem>,
    @InjectRepository(Tender)
    private tenderRepository: Repository<Tender>,
  ) {}

  async findByTender(tenderId: string, tenantId: string) {
    const items = await this.boqItemRepository.find({
      where: { tenderId },
      relations: ['matchedProduct'],
      order: { rowOrder: 'ASC' },
    });

    // Calculate summary
    const subtotal = items.reduce(
      (sum, item) => sum + (item.finalRate || 0) * item.quantity,
      0,
    );
    const totalGst = items.reduce(
      (sum, item) =>
        sum +
        ((item.finalRate || 0) * item.quantity * item.gstPercentage) / 100,
      0,
    );

    return {
      items,
      summary: {
        totalItems: items.length,
        subtotal,
        totalGst,
        grandTotal: subtotal + totalGst,
      },
    };
  }

  async create(
    tenderId: string,
    dto: CreateBOQItemDto,
    tenantId: string,
  ): Promise<BOQItem> {
    const tender = await this.tenderRepository.findOne({
      where: { id: tenderId },
    });

    if (!tender) {
      throw new NotFoundException('Tender not found');
    }

    // Get max row order
    const maxOrder = await this.boqItemRepository
      .createQueryBuilder('boq')
      .where('boq.tenderId = :tenderId', { tenderId })
      .select('MAX(boq.rowOrder)', 'max')
      .getRawOne();

    const item = this.boqItemRepository.create({
      ...dto,
      tenderId,
      rowOrder: (maxOrder?.max || 0) + 1,
      finalRate: dto.manualRate || dto.suggestedRate,
    });

    return this.boqItemRepository.save(item);
  }

  async update(
    id: string,
    dto: UpdateBOQItemDto,
    tenantId: string,
  ): Promise<BOQItem> {
    const item = await this.boqItemRepository.findOne({ where: { id } });

    if (!item) {
      throw new NotFoundException('BOQ item not found');
    }

    // Update final rate if manual rate is provided
    if (dto.manualRate !== undefined) {
      item.finalRate = dto.manualRate;
    }

    Object.assign(item, dto);
    return this.boqItemRepository.save(item);
  }

  async remove(id: string, tenantId: string): Promise<void> {
    const result = await this.boqItemRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException('BOQ item not found');
    }
  }

  async generateFromTender(tenderId: string, tenantId: string) {
    const tender = await this.tenderRepository.findOne({
      where: { id: tenderId },
    });

    if (!tender) {
      throw new NotFoundException('Tender not found');
    }

    // Mock BOQ generation from parsed data
    // In production, this would use NLP to extract items from tender documents
    const mockItems = [
      {
        itemNumber: '1',
        description: 'Sample Item from Tender',
        quantity: 100,
        unit: 'nos',
        suggestedRate: 1000,
        gstPercentage: 18,
      },
    ];

    const items = [];
    for (const mockItem of mockItems) {
      const item = await this.create(tenderId, mockItem as any, tenantId);
      items.push(item);
    }

    return {
      message: 'BOQ generated successfully',
      itemsCreated: items.length,
      items,
    };
  }
}
