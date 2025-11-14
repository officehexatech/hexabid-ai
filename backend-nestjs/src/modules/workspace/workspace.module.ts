import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { TenderProject } from '../../database/entities/tender-project.entity';

@Module({
  imports: [TypeOrmModule.forFeature([TenderProject])],
  exports: [],
})
export class WorkspaceModule {}
