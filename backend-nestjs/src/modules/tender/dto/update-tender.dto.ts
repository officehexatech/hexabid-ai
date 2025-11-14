import { PartialType } from '@nestjs/swagger';
import { IsOptional, IsString, IsArray, IsBoolean } from 'class-validator';
import { CreateTenderDto } from './create-tender.dto';

export class UpdateTenderDto extends PartialType(CreateTenderDto) {
  @IsOptional()
  @IsString()
  status?: string;

  @IsOptional()
  @IsString()
  assignedTo?: string;

  @IsOptional()
  @IsArray()
  tags?: string[];

  @IsOptional()
  @IsBoolean()
  isStarred?: boolean;
}
