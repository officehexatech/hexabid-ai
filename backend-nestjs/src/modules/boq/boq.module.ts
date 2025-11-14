import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BOQController } from './boq.controller';
import { BOQService } from './boq.service';
import { BOQItem } from '../../database/entities/boq-item.entity';
import { Tender } from '../../database/entities/tender.entity';

@Module({
  imports: [TypeOrmModule.forFeature([BOQItem, Tender])],
  controllers: [BOQController],
  providers: [BOQService],
  exports: [BOQService],
})
export class BOQModule {}
