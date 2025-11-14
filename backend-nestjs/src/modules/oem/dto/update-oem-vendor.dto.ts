import { PartialType } from '@nestjs/swagger';
import { CreateOEMVendorDto } from './create-oem-vendor.dto';

export class UpdateOEMVendorDto extends PartialType(CreateOEMVendorDto) {}
