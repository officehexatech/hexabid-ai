import { IsString, IsOptional, IsNumber, IsDate, IsArray } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateTenderDto {
  @ApiProperty()
  @IsString()
  source: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  sourceUrl?: string;

  @ApiProperty()
  @IsString()
  title: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  tenderNumber?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  buyerOrganization?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  category?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  tenderValue?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @Type(() => Date)
  @IsDate()
  bidSubmissionEndDate?: Date;

  @ApiPropertyOptional()
  @IsOptional()
  @IsArray()
  documents?: any[];
}
