import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
} from 'typeorm';
import { SalesOrder } from './sales-order.entity';
import { User } from './user.entity';

@Entity('invoices')
export class Invoice {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true })
  salesOrderId: string;

  @ManyToOne(() => SalesOrder)
  @JoinColumn({ name: 'salesOrderId' })
  salesOrder: SalesOrder;

  @Column({ unique: true })
  invoiceNumber: string;

  @Column({ type: 'date' })
  invoiceDate: Date;

  @Column({ type: 'varchar', default: 'tax_invoice' })
  invoiceType: string;

  @Column()
  customerName: string;

  @Column({ nullable: true })
  customerGstin: string;

  @Column({ type: 'text', nullable: true })
  billingAddress: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  subtotal: number;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  taxAmount: number;

  @Column({ type: 'decimal', precision: 15, scale: 2 })
  totalAmount: number;

  @Column({ type: 'varchar', length: 3, default: 'INR' })
  currency: string;

  @Column({ type: 'varchar', default: 'unpaid' })
  paymentStatus: string;

  @Column({ type: 'date', nullable: true })
  paymentDueDate: Date;

  @Column({ type: 'decimal', precision: 15, scale: 2, default: 0 })
  amountPaid: number;

  @Column({ type: 'text', nullable: true })
  invoicePdfUrl: string;

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

  @Column({ nullable: true })
  sentAt: Date;

  @Column({ nullable: true })
  paidAt: Date;
}
