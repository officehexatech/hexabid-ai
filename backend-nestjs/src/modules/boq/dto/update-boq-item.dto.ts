import { PartialType } from '@nestjs/swagger';
import { CreateBOQItemDto } from './create-boq-item.dto';

export class UpdateBOQItemDto extends PartialType(CreateBOQItemDto) {}
