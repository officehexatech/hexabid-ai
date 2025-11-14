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

@Entity('tender_projects')
export class TenderProject {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  tenderId: string;

  @ManyToOne(() => Tender)
  @JoinColumn({ name: 'tenderId' })
  tender: Tender;

  @Column()
  projectName: string;

  @Column({ unique: true })
  projectCode: string;

  @Column({ nullable: true })
  bidManagerId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'bidManagerId' })
  bidManager: User;

  @Column({ nullable: true })
  techLeadId: string;

  @Column({ nullable: true })
  financeLeadId: string;

  @Column({ type: 'uuid', array: true, default: '{}' })
  teamMembers: string[];

  @Column({ nullable: true })
  bidStrategyProfileId: string;

  @Column({ type: 'decimal', precision: 5, scale: 2, nullable: true })
  targetMarginPercentage: number;

  @Column({ type: 'varchar', default: 'initiated' })
  status: string;

  @Column({ type: 'jsonb', default: [] })
  milestones: any[];

  @Column({ type: 'jsonb', default: {} })
  workspaceSettings: Record<string, any>;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  completedAt: Date;
}
