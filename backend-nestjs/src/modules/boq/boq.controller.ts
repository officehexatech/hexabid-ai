import {
  Controller,
  Get,
  Post,
  Patch,
  Delete,
  Body,
  Param,
  UseGuards,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger';
import { BOQService } from './boq.service';
import { CreateBOQItemDto } from './dto/create-boq-item.dto';
import { UpdateBOQItemDto } from './dto/update-boq-item.dto';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { CurrentTenant } from '../../common/decorators/current-tenant.decorator';

@ApiTags('boq')
@Controller('boq')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class BOQController {
  constructor(private readonly boqService: BOQService) {}

  @Get('tender/:tenderId')
  @ApiOperation({ summary: 'Get BOQ items for a tender' })
  async findByTender(
    @Param('tenderId') tenderId: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.boqService.findByTender(tenderId, tenantId);
  }

  @Post('tender/:tenderId/items')
  @ApiOperation({ summary: 'Add BOQ item' })
  async create(
    @Param('tenderId') tenderId: string,
    @Body() dto: CreateBOQItemDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.boqService.create(tenderId, dto, tenantId);
  }

  @Patch('items/:id')
  @ApiOperation({ summary: 'Update BOQ item' })
  async update(
    @Param('id') id: string,
    @Body() dto: UpdateBOQItemDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.boqService.update(id, dto, tenantId);
  }

  @Delete('items/:id')
  @ApiOperation({ summary: 'Delete BOQ item' })
  async remove(
    @Param('id') id: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.boqService.remove(id, tenantId);
  }

  @Post('tender/:tenderId/generate')
  @ApiOperation({ summary: 'Auto-generate BOQ from tender' })
  async generate(
    @Param('tenderId') tenderId: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.boqService.generateFromTender(tenderId, tenantId);
  }
}
