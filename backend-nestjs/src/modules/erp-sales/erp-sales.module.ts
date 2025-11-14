import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SalesOrder } from '../../database/entities/sales-order.entity';
import { Invoice } from '../../database/entities/invoice.entity';

@Module({
  imports: [TypeOrmModule.forFeature([SalesOrder, Invoice])],
  exports: [],
})
export class ERPSalesModule {}
