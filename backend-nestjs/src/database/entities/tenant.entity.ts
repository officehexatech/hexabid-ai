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

  @Column({ unique: true })
  subdomain: string;

  @Column()
  companyName: string;

  @Column({ nullable: true })
  companyEmail: string;

  @Column({ nullable: true })
  companyPhone: string;

  @Column({ type: 'varchar', default: 'active' })
  status: string;

  @Column({ type: 'int', default: 10 })
  userLimit: number;

  @Column({ type: 'int', default: 50 })
  storageLimitGb: number;

  @Column({ type: 'jsonb', default: {} })
  settings: Record<string, any>;

  @Column({ nullable: true })
  databaseSchema: string;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;

  @Column({ nullable: true })
  deletedAt: Date;
}
