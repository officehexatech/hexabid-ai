import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Product } from '../../database/entities/product.entity';
import { OEMVendor } from '../../database/entities/oem-vendor.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Product, OEMVendor])],
  exports: [],
})
export class ProductModule {}
