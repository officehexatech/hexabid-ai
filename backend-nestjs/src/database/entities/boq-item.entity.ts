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
import { Product } from './product.entity';

@Entity('boq_items')
export class BOQItem {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  tenderId: string;

  @ManyToOne(() => Tender)
  @JoinColumn({ name: 'tenderId' })
  tender: Tender;

  @Column({ nullable: true })
  itemNumber: string;

  @Column({ type: 'text' })
  description: string;

  @Column({ type: 'text', nullable: true })
  specifications: string;

  @Column({ nullable: true })
  hsnCode: string;

  @Column({ type: 'decimal', precision: 12, scale: 2 })
  quantity: number;

  @Column()
  unit: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  suggestedRate: number;

  @Column({ nullable: true })
  suggestedRateSource: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  manualRate: number;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  finalRate: number;

  @Column({ type: 'decimal', precision: 5, scale: 2, default: 18.0 })
  gstPercentage: number;

  @Column({ nullable: true })
  matchedProductId: string;

  @ManyToOne(() => Product)
  @JoinColumn({ name: 'matchedProductId' })
  matchedProduct: Product;

  @Column({ type: 'decimal', precision: 3, scale: 2, nullable: true })
  matchingConfidence: number;

  @Column({ nullable: true })
  selectedVendorQuoteId: string;

  @Column({ type: 'text', nullable: true })
  notes: string;

  @Column({ nullable: true })
  formula: string;

  @Column({ type: 'int', nullable: true })
  rowOrder: number;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
