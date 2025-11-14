import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { OEMVendor } from '../../database/entities/oem-vendor.entity';

@Module({
  imports: [TypeOrmModule.forFeature([OEMVendor])],
  exports: [],
})
export class OEMModule {}
