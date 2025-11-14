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
import { User } from './user.entity';

@Entity('sales_orders')
export class SalesOrder {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true })
  tenderId: string;

  @ManyToOne(() => Tender)
  @JoinColumn({ name: 'tenderId' })
  tender: Tender;

  @Column({ unique: true })
  orderNumber: string;

  @Column({ type: 'date' })
  orderDate: Date;

  @Column()
  customerName: string;

  @Column({ nullable: true })
  customerOrganization: string;

  @Column({ nullable: true })
  customerGstin: string;

  @Column({ nullable: true })
  customerPan: string;

  @Column({ type: 'text', nullable: true })
  billingAddress: string;

  @Column({ type: 'text', nullable: true })
  shippingAddress: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  subtotal: number;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  taxAmount: number;

  @Column({ type: 'decimal', precision: 15, scale: 2 })
  totalAmount: number;

  @Column({ type: 'varchar', length: 3, default: 'INR' })
  currency: string;

  @Column({ nullable: true })
  paymentTerms: string;

  @Column({ type: 'date', nullable: true })
  paymentDueDate: Date;

  @Column({ type: 'date', nullable: true })
  expectedDeliveryDate: Date;

  @Column({ type: 'varchar', default: 'pending' })
  deliveryStatus: string;

  @Column({ type: 'varchar', default: 'draft' })
  status: string;

  @Column({ type: 'text', nullable: true })
  notes: string;

  @Column({ nullable: true })
  createdBy: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'createdBy' })
  creator: User;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
