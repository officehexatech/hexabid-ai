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

@Entity('tenders')
export class Tender {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  source: string; // gem, manual_upload, paste_url, csv_import

  @Column({ type: 'text', nullable: true })
  sourceUrl: string;

  @Column({ nullable: true })
  externalTenderId: string;

  @Column({ type: 'text' })
  title: string;

  @Column({ nullable: true })
  tenderNumber: string;

  @Column({ nullable: true })
  buyerOrganization: string;

  @Column({ nullable: true })
  buyerDepartment: string;

  @Column({ nullable: true })
  category: string;

  @Column({ nullable: true })
  subCategory: string;

  @Column({ nullable: true })
  tenderType: string;

  @Column({ type: 'decimal', precision: 15, scale: 2, nullable: true })
  tenderValue: number;

  @Column({ type: 'varchar', length: 3, default: 'INR' })
  currency: string;

  @Column({ type: 'date', nullable: true })
  publishedDate: Date;

  @Column({ type: 'timestamp', nullable: true })
  bidSubmissionStartDate: Date;

  @Column({ type: 'timestamp', nullable: true })
  bidSubmissionEndDate: Date;

  @Column({ type: 'timestamp', nullable: true })
  technicalBidOpeningDate: Date;

  @Column({ type: 'timestamp', nullable: true })
  financialBidOpeningDate: Date;

  @Column({ nullable: true })
  tenderLocation: string;

  @Column({ nullable: true })
  state: string;

  @Column({ nullable: true })
  region: string;

  @Column({ type: 'jsonb', default: [] })
  documents: any[];

  @Column({ type: 'varchar', default: 'pending' })
  parsingStatus: string;

  @Column({ type: 'jsonb', nullable: true })
  parsedData: any;

  @Column({ type: 'decimal', precision: 3, scale: 2, nullable: true })
  parsingConfidence: number;

  @Column({ type: 'text', nullable: true })
  eligibilityCriteria: string;

  @Column({ type: 'text', nullable: true })
  technicalRequirements: string;

  @Column({ type: 'text', nullable: true })
  specialConditions: string;

  @Column({ type: 'varchar', default: 'discovered' })
  status: string;

  @Column({ type: 'decimal', precision: 3, scale: 2, nullable: true })
  matchScore: number;

  @Column({ type: 'boolean', default: false })
  isStarred: boolean;

  @Column({ type: 'text', array: true, default: '{}' })
  tags: string[];

  @Column({ nullable: true })
  assignedTo: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'assignedTo' })
  assignedUser: User;

  @Column({ nullable: true })
  assignedAt: Date;

  @Column({ nullable: true })
  createdBy: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  deletedAt: Date;
}
