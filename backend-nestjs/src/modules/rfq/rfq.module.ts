import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { RFQRequest } from '../../database/entities/rfq-request.entity';
import { VendorQuote } from '../../database/entities/vendor-quote.entity';

@Module({
  imports: [TypeOrmModule.forFeature([RFQRequest, VendorQuote])],
  exports: [],
})
export class RFQModule {}
