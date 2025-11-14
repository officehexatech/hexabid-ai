import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { OEMVendor } from '../../database/entities/oem-vendor.entity';
import { VendorQuote } from '../../database/entities/vendor-quote.entity';
import { OEMController } from './oem.controller';
import { OEMService } from './oem.service';

@Module({
  imports: [TypeOrmModule.forFeature([OEMVendor, VendorQuote])],
  controllers: [OEMController],
  providers: [OEMService],
  exports: [OEMService],
})
export class OEMModule {}
