import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
  CreateDateColumn,
} from 'typeorm';
import { User } from './user.entity';

@Entity('notifications')
export class Notification {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  userId: string;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'userId' })
  user: User;

  @Column()
  type: string;

  @Column()
  title: string;

  @Column({ type: 'text', nullable: true })
  message: string;

  @Column({ nullable: true })
  relatedResourceType: string;

  @Column({ nullable: true })
  relatedResourceId: string;

  @Column({ type: 'varchar', array: true, default: '{}' })
  channels: string[];

  @Column({ type: 'boolean', default: false })
  isRead: boolean;

  @Column({ nullable: true })
  readAt: Date;

  @Column({ type: 'text', nullable: true })
  actionUrl: string;

  @Column({ nullable: true })
  actionLabel: string;

  @CreateDateColumn()
  createdAt: Date;
}
