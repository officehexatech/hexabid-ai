import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { Tender } from './tender.entity';
import { OEMVendor } from './oem-vendor.entity';
import { RFQRequest } from './rfq-request.entity';

@Entity('vendor_quotes')
export class VendorQuote {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  tenderId: string;

  @ManyToOne(() => Tender)
  @JoinColumn({ name: 'tenderId' })
  tender: Tender;

  @Column()
  vendorId: string;

  @ManyToOne(() => OEMVendor)
  @JoinColumn({ name: 'vendorId' })
  vendor: OEMVendor;

  @Column({ nullable: true })
  rfqId: string;

  @ManyToOne(() => RFQRequest)
  @JoinColumn({ name: 'rfqId' })
  rfq: RFQRequest;

  @Column({ nullable: true })
  quoteNumber: string;

  @Column({ type: 'date', nullable: true })
  quoteDate: Date;

  @Column({ type: 'date', nullable: true })
  validUntil: Date;

  @Column({ type: 'varchar', length: 3, default: 'INR' })
  currency: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  totalAmount: number;

  @Column({ type: 'jsonb', default: [] })
  lineItems: any[];

  @Column({ nullable: true })
  paymentTerms: string;

  @Column({ nullable: true })
  deliveryTerms: string;

  @Column({ nullable: true })
  warrantyTerms: string;

  @Column({ type: 'text', nullable: true })
  quoteDocumentUrl: string;

  @Column({ type: 'varchar', default: 'received' })
  status: string;

  @Column({ type: 'text', nullable: true })
  internalNotes: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
