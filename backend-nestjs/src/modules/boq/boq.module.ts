import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BOQItem } from '../../database/entities/boq-item.entity';
import { Tender } from '../../database/entities/tender.entity';

@Module({
  imports: [TypeOrmModule.forFeature([BOQItem, Tender])],
  exports: [],
})
export class BOQModule {}
