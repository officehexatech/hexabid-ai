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

@Entity('document_assembly_jobs')
export class DocumentAssemblyJob {
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

  @Column({ nullable: true })
  jobName: string;

  @Column({ type: 'uuid', array: true, default: '{}' })
  templateIds: string[];

  @Column({ type: 'jsonb' })
  mergeData: Record<string, any>;

  @Column({ type: 'varchar', default: 'pdf' })
  outputFormat: string;

  @Column({ nullable: true })
  outputStructure: string;

  @Column({ nullable: true })
  namingConvention: string;

  @Column({ type: 'varchar', default: 'queued' })
  status: string;

  @Column({ type: 'int', default: 0 })
  progressPercentage: number;

  @Column({ type: 'text', nullable: true })
  errorMessage: string;

  @Column({ type: 'text', nullable: true })
  outputFileUrl: string;

  @Column({ type: 'int', nullable: true })
  outputFileSize: number;

  @Column({ nullable: true })
  createdBy: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'createdBy' })
  creator: User;

  @CreateDateColumn()
  createdAt: Date;

  @Column({ nullable: true })
  startedAt: Date;

  @Column({ nullable: true })
  completedAt: Date;
}
