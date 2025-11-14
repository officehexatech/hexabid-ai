import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { TenderController } from './tender.controller';
import { TenderService } from './tender.service';
import { Tender } from '../../database/entities/tender.entity';
import { User } from '../../database/entities/user.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Tender, User])],
  controllers: [TenderController],
  providers: [TenderService],
  exports: [TenderService],
})
export class TenderModule {}
