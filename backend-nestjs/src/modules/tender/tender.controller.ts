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
import { TenderService } from './tender.service';
import { CreateTenderDto } from './dto/create-tender.dto';
import { UpdateTenderDto } from './dto/update-tender.dto';
import { SearchTendersDto } from './dto/search-tenders.dto';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { CurrentUser } from '../../common/decorators/current-user.decorator';
import { CurrentTenant } from '../../common/decorators/current-tenant.decorator';

@ApiTags('tenders')
@Controller('tenders')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class TenderController {
  constructor(private readonly tenderService: TenderService) {}

  @Get()
  @ApiOperation({ summary: 'List all tenders with search and filters' })
  async findAll(
    @Query() query: SearchTendersDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.tenderService.findAll(query, tenantId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get tender by ID' })
  async findOne(@Param('id') id: string, @CurrentTenant() tenantId: string) {
    return this.tenderService.findOne(id, tenantId);
  }

  @Post()
  @ApiOperation({ summary: 'Create new tender (manual upload)' })
  async create(
    @Body() dto: CreateTenderDto,
    @CurrentUser() user: any,
    @CurrentTenant() tenantId: string,
  ) {
    return this.tenderService.create(dto, user.id, tenantId);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update tender' })
  async update(
    @Param('id') id: string,
    @Body() dto: UpdateTenderDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.tenderService.update(id, dto, tenantId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete tender (soft delete)' })
  async remove(@Param('id') id: string, @CurrentTenant() tenantId: string) {
    return this.tenderService.remove(id, tenantId);
  }
}
