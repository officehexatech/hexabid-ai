-- Initialize HexaBid Database

-- Create public schema tables (shared across tenants)
CREATE TABLE IF NOT EXISTS public.tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subdomain VARCHAR(100) UNIQUE NOT NULL,
  company_name VARCHAR(255) NOT NULL,
  company_email VARCHAR(255),
  company_phone VARCHAR(20),
  status VARCHAR(20) DEFAULT 'active',
  user_limit INTEGER DEFAULT 10,
  storage_limit_gb INTEGER DEFAULT 50,
  settings JSONB DEFAULT '{}',
  database_schema VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

-- Insert demo tenant
INSERT INTO public.tenants (subdomain, company_name, company_email, status)
VALUES 
  ('demo', 'Demo Corporation', 'demo@hexabid.in', 'active'),
  ('acme', 'ACME Industries', 'contact@acme.com', 'active')
ON CONFLICT (subdomain) DO NOTHING;

CREATE INDEX IF NOT EXISTS idx_tenants_subdomain ON public.tenants(subdomain);
CREATE INDEX IF NOT EXISTS idx_tenants_status ON public.tenants(status);

COMMIT;
