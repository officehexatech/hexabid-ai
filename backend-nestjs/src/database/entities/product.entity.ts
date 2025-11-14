import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { OEMVendor } from './oem-vendor.entity';

@Entity('products')
export class Product {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true })
  sku: string;

  @Column()
  productName: string;

  @Column({ nullable: true })
  brand: string;

  @Column({ nullable: true })
  model: string;

  @Column({ nullable: true })
  oemVendorId: string;

  @ManyToOne(() => OEMVendor)
  @JoinColumn({ name: 'oemVendorId' })
  oemVendor: OEMVendor;

  @Column({ nullable: true })
  category: string;

  @Column({ nullable: true })
  subCategory: string;

  @Column({ type: 'jsonb', default: {} })
  specifications: Record<string, any>;

  @Column({ type: 'text', nullable: true })
  technicalDescription: string;

  @Column({ nullable: true })
  hsnCode: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  listPrice: number;

  @Column({ type: 'varchar', length: 3, default: 'INR' })
  currency: string;

  @Column({ type: 'int', nullable: true })
  leadTimeDays: number;

  @Column({ nullable: true })
  stockStatus: string;

  @Column({ type: 'jsonb', default: [] })
  images: string[];

  @Column({ type: 'jsonb', default: [] })
  datasheets: string[];

  @Column({ type: 'jsonb', default: [] })
  certifications: string[];

  @Column({ type: 'boolean', default: true })
  isActive: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
