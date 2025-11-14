import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
} from 'typeorm';
import { Tender } from './tender.entity';
import { TenderProject } from './tender-project.entity';
import { User } from './user.entity';

@Entity('rfq_requests')
export class RFQRequest {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  tenderId: string;

  @ManyToOne(() => Tender)
  @JoinColumn({ name: 'tenderId' })
  tender: Tender;

  @Column({ nullable: true })
  projectId: string;

  @ManyToOne(() => TenderProject)
  @JoinColumn({ name: 'projectId' })
  project: TenderProject;

  @Column({ unique: true })
  rfqNumber: string;

  @Column()
  subject: string;

  @Column({ type: 'text' })
  message: string;

  @Column({ type: 'uuid', array: true, default: '{}' })
  boqItemIds: string[];

  @Column({ type: 'uuid', array: true, default: '{}' })
  vendorIds: string[];

  @Column({ type: 'timestamp', nullable: true })
  responseDeadline: Date;

  @Column({ type: 'varchar', array: true, default: '{}' })
  sentVia: string[]; // email, whatsapp

  @Column({ type: 'jsonb', default: {} })
  emailStatus: Record<string, string>;

  @Column({ type: 'jsonb', default: {} })
  whatsappStatus: Record<string, string>;

  @Column({ type: 'int', default: 0 })
  totalSent: number;

  @Column({ type: 'int', default: 0 })
  totalResponses: number;

  @Column({ type: 'varchar', default: 'draft' })
  status: string;

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
  closedAt: Date;
}
