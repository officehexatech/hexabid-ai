import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';
import { TenantMiddleware } from './common/middleware/tenant.middleware';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Global prefix
  app.setGlobalPrefix(process.env.API_PREFIX || 'api');

  // CORS
  app.enableCors({
    origin: process.env.FRONTEND_URL || 'http://localhost:3001',
    credentials: true,
  });

  // Global validation pipe
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      transform: true,
      forbidNonWhitelisted: true,
    }),
  );

  // Swagger documentation
  const config = new DocumentBuilder()
    .setTitle('HexaBid API')
    .setDescription('Multi-tenant Tender & ERP Platform API')
    .setVersion('1.0')
    .addBearerAuth()
    .addTag('auth', 'Authentication')
    .addTag('tenders', 'Tender Management')
    .addTag('boq', 'Bill of Quantities')
    .addTag('products', 'Product Catalog')
    .addTag('oem', 'OEM/Vendor Management')
    .addTag('rfq', 'Request for Quotation')
    .addTag('documents', 'Document Assembly')
    .addTag('compliance', 'Compliance & Approvals')
    .addTag('ai', 'AI Assistant')
    .addTag('erp-sales', 'ERP - Sales')
    .addTag('erp-purchase', 'ERP - Purchase')
    .addTag('erp-inventory', 'ERP - Inventory')
    .addTag('erp-projects', 'ERP - Projects')
    .addTag('erp-accounting', 'ERP - Accounting')
    .addTag('erp-hrms', 'ERP - HRMS')
    .addTag('analytics', 'Analytics & MIS')
    .addTag('admin', 'Administration')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);

  const port = process.env.PORT || 3000;
  await app.listen(port);

  console.log(`\n🚀 HexaBid Backend running on: http://localhost:${port}`);
  console.log(`📚 API Documentation: http://localhost:${port}/api/docs\n`);
}

bootstrap();
