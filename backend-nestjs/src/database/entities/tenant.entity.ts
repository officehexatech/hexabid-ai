import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('tenants', { schema: 'public' })
export class Tenant {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true, nullable: true })
  subdomain: string | null;

  @Column({ nullable: true })
  companyName: string | null;

  @Column({ nullable: true })
  companyEmail: string | null;

  @Column({ nullable: true })
  companyPhone: string | null;

  @Column({ type: 'varchar', default: 'active' })
  status: string;

  @Column({ type: 'int', nullable: true, default: 10 })
  userLimit: number | null;

  @Column({ type: 'int', nullable: true, default: 50 })
  storageLimitGb: number | null;

  @Column({ type: 'jsonb', default: {} })
  settings: Record<string, any>;

  @Column({ nullable: true })
  databaseSchema: string | null;

  @CreateDateColumn({ nullable: true })
  createdAt: Date | null;

  @UpdateDateColumn({ nullable: true })
  updatedAt: Date | null;

  @Column({ nullable: true })
  deletedAt: Date | null;
}
