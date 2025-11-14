import { Module, MiddlewareConsumer, NestModule } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BullModule } from '@nestjs/bull';
import { ScheduleModule } from '@nestjs/schedule';
import { TenantMiddleware } from './common/middleware/tenant.middleware';
import { AuthModule } from './modules/auth/auth.module';
import { TenantModule } from './modules/tenant/tenant.module';
import { TenderModule } from './modules/tender/tender.module';
import { BOQModule } from './modules/boq/boq.module';
import { ProductModule } from './modules/product/product.module';
import { OEMModule } from './modules/oem/oem.module';
import { RFQModule } from './modules/rfq/rfq.module';
import { DocumentModule } from './modules/document/document.module';
import { ComplianceModule } from './modules/compliance/compliance.module';
import { WorkspaceModule } from './modules/workspace/workspace.module';
import { AIModule } from './modules/ai/ai.module';
import { ERPSalesModule } from './modules/erp-sales/erp-sales.module';
import { ERPPurchaseModule } from './modules/erp-purchase/erp-purchase.module';
import { ERPInventoryModule } from './modules/erp-inventory/erp-inventory.module';
import { ERPProjectModule } from './modules/erp-project/erp-project.module';
import { ERPAccountingModule } from './modules/erp-accounting/erp-accounting.module';
import { ERPHRMSModule } from './modules/erp-hrms/erp-hrms.module';
import { AnalyticsModule } from './modules/analytics/analytics.module';
import { NotificationModule } from './modules/notification/notification.module';
import { AdminModule } from './modules/admin/admin.module';

@Module({
  imports: [
    // Configuration
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // Database
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        type: 'postgres',
        host: configService.get('DATABASE_HOST'),
        port: configService.get('DATABASE_PORT'),
        username: configService.get('DATABASE_USERNAME'),
        password: configService.get('DATABASE_PASSWORD'),
        database: configService.get('DATABASE_NAME'),
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: configService.get('NODE_ENV') === 'development', // Only in dev
        logging: configService.get('NODE_ENV') === 'development',
      }),
    }),

    // Redis & Bull Queue
    BullModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (configService: ConfigService) => ({
        redis: {
          host: configService.get('REDIS_HOST'),
          port: configService.get('REDIS_PORT'),
          password: configService.get('REDIS_PASSWORD'),
        },
      }),
    }),

    // Schedule (for cron jobs)
    ScheduleModule.forRoot(),

    // Application Modules
    AuthModule,
    TenantModule,
    TenderModule,
    BOQModule,
    ProductModule,
    OEMModule,
    RFQModule,
    DocumentModule,
    ComplianceModule,
    WorkspaceModule,
    AIModule,
    ERPSalesModule,
    ERPPurchaseModule,
    ERPInventoryModule,
    ERPProjectModule,
    ERPAccountingModule,
    ERPHRMSModule,
    AnalyticsModule,
    NotificationModule,
    AdminModule,
  ],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(TenantMiddleware).forRoutes('*');
  }
}
