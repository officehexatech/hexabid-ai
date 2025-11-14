import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';
import { User } from './user.entity';

@Entity('employees')
export class Employee {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ nullable: true, unique: true })
  userId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'userId' })
  user: User;

  @Column({ unique: true })
  employeeCode: string;

  @Column()
  firstName: string;

  @Column({ nullable: true })
  lastName: string;

  @Column({ type: 'date', nullable: true })
  dateOfBirth: Date;

  @Column({ nullable: true })
  gender: string;

  @Column({ nullable: true })
  personalEmail: string;

  @Column({ nullable: true })
  workEmail: string;

  @Column({ nullable: true })
  mobilePhone: string;

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
  department: string;

  @Column({ nullable: true })
  designation: string;

  @Column({ nullable: true })
  employmentType: string;

  @Column({ type: 'date', nullable: true })
  dateOfJoining: Date;

  @Column({ type: 'date', nullable: true })
  dateOfLeaving: Date;

  @Column({ nullable: true })
  reportsTo: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  salaryAmount: number;

  @Column({ type: 'varchar', length: 3, default: 'INR' })
  salaryCurrency: string;

  @Column({ nullable: true, default: 'monthly' })
  salaryFrequency: string;

  @Column({ nullable: true })
  bankName: string;

  @Column({ nullable: true })
  bankAccountNumber: string;

  @Column({ nullable: true })
  bankIfsc: string;

  @Column({ nullable: true })
  pan: string;

  @Column({ nullable: true })
  aadhar: string;

  @Column({ type: 'jsonb', default: [] })
  documents: any[];

  @Column({ type: 'varchar', default: 'active' })
  status: string;

  @Column({ type: 'text', nullable: true })
  notes: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
