import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { DocumentTemplate } from '../../database/entities/document-template.entity';
import { DocumentAssemblyJob } from '../../database/entities/document-assembly-job.entity';

@Module({
  imports: [TypeOrmModule.forFeature([DocumentTemplate, DocumentAssemblyJob])],
  exports: [],
})
export class DocumentModule {}
