import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('oem_vendors')
export class OEMVendor {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  companyName: string;

  @Column({ nullable: true })
  vendorType: string;

  @Column({ nullable: true })
  primaryContactName: string;

  @Column({ nullable: true })
  primaryContactEmail: string;

  @Column({ nullable: true })
  primaryContactPhone: string;

  @Column({ type: 'jsonb', default: [] })
  contacts: any[];

  @Column({ type: 'text', nullable: true })
  address: string;

  @Column({ nullable: true })
  city: string;

  @Column({ nullable: true })
  state: string;

  @Column({ nullable: true, default: 'India' })
  country: string;

  @Column({ nullable: true })
  pincode: string;

  @Column({ nullable: true })
  gstin: string;

  @Column({ nullable: true })
  pan: string;

  @Column({ nullable: true })
  website: string;

  @Column({ type: 'decimal', precision: 2, scale: 1, nullable: true })
  rating: number;

  @Column({ type: 'int', default: 0 })
  totalRfqsSent: number;

  @Column({ type: 'int', default: 0 })
  totalQuotesReceived: number;

  @Column({ type: 'int', nullable: true })
  avgResponseTimeHours: number;

  @Column({ nullable: true })
  paymentTerms: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  creditLimit: number;

  @Column({ type: 'text', array: true, default: '{}' })
  categories: string[];

  @Column({ type: 'text', array: true, default: '{}' })
  tags: string[];

  @Column({ type: 'text', nullable: true })
  notes: string;

  @Column({ type: 'boolean', default: true })
  isActive: boolean;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
