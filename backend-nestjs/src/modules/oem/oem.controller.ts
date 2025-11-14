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
import { OEMService } from './oem.service';
import { CreateOEMVendorDto } from './dto/create-oem-vendor.dto';
import { UpdateOEMVendorDto } from './dto/update-oem-vendor.dto';
import { SearchVendorsDto } from './dto/search-vendors.dto';
import { JwtAuthGuard } from '../../common/guards/jwt-auth.guard';
import { CurrentTenant } from '../../common/decorators/current-tenant.decorator';
import { CurrentUser } from '../../common/decorators/current-user.decorator';

@ApiTags('oem')
@Controller('oem-vendors')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class OEMController {
  constructor(private readonly oemService: OEMService) {}

  @Get()
  @ApiOperation({ summary: 'List OEM vendors' })
  async findAll(
    @Query() query: SearchVendorsDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.oemService.findAll(query, tenantId);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get vendor details' })
  async findOne(
    @Param('id') id: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.oemService.findOne(id, tenantId);
  }

  @Post()
  @ApiOperation({ summary: 'Create OEM vendor' })
  async create(
    @Body() dto: CreateOEMVendorDto,
    @CurrentUser() user: any,
    @CurrentTenant() tenantId: string,
  ) {
    return this.oemService.create(dto, tenantId);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update vendor' })
  async update(
    @Param('id') id: string,
    @Body() dto: UpdateOEMVendorDto,
    @CurrentTenant() tenantId: string,
  ) {
    return this.oemService.update(id, dto, tenantId);
  }

  @Delete(':id')
  @ApiOperation({ summary: 'Delete vendor' })
  async remove(
    @Param('id') id: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.oemService.remove(id, tenantId);
  }

  @Get(':id/quotes')
  @ApiOperation({ summary: 'Get quotes from vendor' })
  async getQuotes(
    @Param('id') id: string,
    @CurrentTenant() tenantId: string,
  ) {
    return this.oemService.getVendorQuotes(id, tenantId);
  }
}
