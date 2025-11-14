import { IsString, IsNumber, IsOptional, Min } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateBOQItemDto {
  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  itemNumber?: string;

  @ApiProperty()
  @IsString()
  description: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  specifications?: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  hsnCode?: string;

  @ApiProperty()
  @IsNumber()
  @Min(0)
  quantity: number;

  @ApiProperty()
  @IsString()
  unit: string;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  suggestedRate?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsNumber()
  manualRate?: number;

  @ApiPropertyOptional({ default: 18 })
  @IsOptional()
  @IsNumber()
  gstPercentage?: number;

  @ApiPropertyOptional()
  @IsOptional()
  @IsString()
  notes?: string;
}
