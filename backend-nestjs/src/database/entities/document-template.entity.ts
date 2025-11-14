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

@Entity('document_templates')
export class DocumentTemplate {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column({ nullable: true })
  templateType: string;

  @Column({ type: 'text', nullable: true })
  description: string;

  @Column({ type: 'text' })
  fileUrl: string;

  @Column({ type: 'int', nullable: true })
  fileSize: number;

  @Column({ type: 'jsonb', default: [] })
  mergeFields: any[];

  @Column({ nullable: true })
  category: string;

  @Column({ type: 'boolean', default: false })
  isDefault: boolean;

  @Column({ type: 'int', default: 0 })
  usageCount: number;

  @Column({ nullable: true, default: '1.0' })
  version: string;

  @Column({ type: 'boolean', default: true })
  isActive: boolean;

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
