import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Body,
  Param,
  Query,
  UseGuards,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { ProductService } from './product.service';
import { CreateProductDto } from './dto/create-product.dto';
import { UpdateProductDto } from './dto/update-product.dto';
import { SearchProductsDto } from './dto/search-products.dto';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { CurrentTenant } from '../../common/decorators/current-tenant.decorator';

@ApiTags('products')
@Controller('products')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class ProductController {
  constructor(private readonly productService: ProductService) {}

  @Get()
  @ApiOperation({ summary: 'List products' })
  async findAll(
    @Query() query: SearchProductsDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.productService.findAll(query, tenantId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get product details' })
  async findOne(
    @Param('id') id: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.productService.findOne(id, tenantId);
  }

  @Post()
  @ApiOperation({ summary: 'Create product' })
  async create(
    @Body() dto: CreateProductDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.productService.create(dto, tenantId);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update product' })
  async update(
    @Param('id') id: string,
    @Body() dto: UpdateProductDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.productService.update(id, dto, tenantId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete product' })
  async remove(
    @Param('id') id: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.productService.remove(id, tenantId);
  }

  @Post('match')
  @ApiOperation({ summary: 'Find matching products for BOQ item' })
  async match(
    @Body() dto: { description: string; specifications?: string },
    @CurrentTenant() tenantId: string,
  ) {
    return this.productService.findMatches(dto, tenantId);
  }
}
