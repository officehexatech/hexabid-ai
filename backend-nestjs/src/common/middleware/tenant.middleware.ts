import { Injectable, NestMiddleware } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class TenantMiddleware implements NestMiddleware {
  use(req: Request, res: Response, next: NextFunction) {
    // Extract tenant from subdomain or header
    const host = req.headers.host || '';
    const subdomain = host.split('.')[0];

    // Check X-Tenant-ID header (for API clients)
    const tenantIdHeader = req.headers['x-tenant-id'] as string;

    // Set tenant context
    if (tenantIdHeader) {
      req['tenantId'] = tenantIdHeader;
    } else if (subdomain && subdomain !== 'www' && subdomain !== 'localhost') {
      req['tenantId'] = subdomain;
    }

    next();
  }
}
