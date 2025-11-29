# HexaBid - Super Admin Panel

## 🔐 Overview

The Super Admin Panel provides complete administrative control over all tenants, users, and system operations in the HexaBid platform.

## Access URL

**Frontend:** https://hexabid.in/super-admin
**Backend API:** https://hexabid.in/api/super-admin/*

## Authentication & Authorization

### Super Admin Access
Super admin access is granted to users who:
1. Have their user ID in the `SUPER_ADMIN_IDS` list
2. Have an email ending with `@hexabid.com`

**Default Configuration:**
```python
# Backend: /app/backend/routers/super_admin.py
SUPER_ADMIN_IDS = ["super_admin_user_id"]

def is_super_admin(user: User) -> bool:
    return user.id in SUPER_ADMIN_IDS or user.email.endswith("@hexabid.com")
```

### To Grant Super Admin Access:
1. Add user ID to `SUPER_ADMIN_IDS` list in `/app/backend/routers/super_admin.py`
2. Or register with an email @hexabid.com domain
3. Restart backend service

## Features

### 1. Dashboard Tab 📊

#### Key Metrics Displayed:
- **Tenant Statistics:**
  - Total Tenants
  - Active Tenants
  - Trial Tenants
  - Suspended Tenants

- **Plans Distribution:**
  - Free Plan Count
  - Startup Plan Count
  - Professional Plan Count
  - Enterprise Plan Count

- **Revenue Metrics:**
  - Monthly Recurring Revenue (MRR)
  - Currency: INR

- **Growth Metrics:**
  - Recent Signups (Last 30 days)
  - Total Active Users

- **AI Usage Statistics (Current Month):**
  - Total AI Credits Used
  - Total Tokens Consumed
  - Total Cost Incurred

**API Endpoint:** `GET /api/super-admin/dashboard`

### 2. Tenants Management Tab 🏢

#### Features:
- **View All Tenants** with pagination
- **Filter by:**
  - Status (active, trial, suspended, cancelled)
  - Plan (free, startup, professional, enterprise)

#### Tenant Information Displayed:
- Tenant Name & ID
- Current Plan
- Status
- Member Count
- Creation Date

#### Actions Available:
- **Update Tenant Status:**
  - Active
  - Trial
  - Suspended
  - Cancelled
  - Requires reason for change

- **Update Tenant Plan:**
  - Free
  - Startup
  - Professional
  - Enterprise
  - Requires reason for change

- **View Tenant Details:**
  - Complete tenant information
  - Member list
  - Usage history (last 6 months)
  - Billing history (last 12 months)
  - Current month usage stats

**API Endpoints:**
- `GET /api/super-admin/tenants` - List all tenants
- `GET /api/super-admin/tenants/{tenant_id}` - Get tenant details
- `PATCH /api/super-admin/tenants/{tenant_id}/status` - Update status
- `PATCH /api/super-admin/tenants/{tenant_id}/plan` - Update plan

### 3. Action Log Tab 📝

#### Features:
- View complete audit trail of all admin actions
- Pagination support (50 actions per page)

#### Information Logged:
- Action Type (e.g., update_tenant_status, update_tenant_plan)
- Admin User ID who performed the action
- Target Tenant ID
- Action Details (including reason)
- Timestamp

**API Endpoint:** `GET /api/super-admin/actions`

## Plan Pricing Configuration

Defined in: `/app/backend/models_tenant.py`

```python
PLAN_PRICING = {
    "free": 0,           # ₹0/month
    "startup": 2999,     # ₹2,999/month
    "professional": 9999, # ₹9,999/month
    "enterprise": 29999   # ₹29,999/month
}
```

## Tenant Status Options

- **active** - Fully operational
- **trial** - In trial period
- **suspended** - Temporarily disabled
- **cancelled** - Permanently closed

## Database Collections

The Super Admin Panel interacts with:
- `tenants` - Tenant information
- `tenant_members` - Tenant users/members
- `tenant_usage` - Monthly usage tracking
- `tenant_billing` - Billing history
- `admin_actions` - Audit log

## UI Components

### Dashboard View
- Statistics cards with color coding
- Plan distribution charts
- Revenue and growth metrics
- Usage statistics for current month

### Tenants Table View
- Sortable columns
- Inline status/plan updates
- Quick actions menu
- Detailed tenant modal

### Action Log View
- Chronological list of all actions
- Searchable and filterable
- Detailed action information

## Security Features

1. **Role-Based Access Control:**
   - Only super admins can access the panel
   - 403 Forbidden error for non-super admin users

2. **Audit Trail:**
   - All actions logged with timestamp
   - Reason required for status/plan changes
   - Admin user ID tracked

3. **CORS Protection:**
   - Only allowed domains can access API
   - Configured in backend .env

## Usage Instructions

### For Developers:

1. **Grant Super Admin Access:**
   ```python
   # Edit /app/backend/routers/super_admin.py
   SUPER_ADMIN_IDS = ["user123", "user456"]  # Add user IDs
   ```

2. **Access Panel:**
   - Navigate to: https://hexabid.in/super-admin
   - Login with super admin credentials

3. **Manage Tenants:**
   - Switch to Tenants tab
   - Use dropdown menus to update status/plan
   - Click "View Details" for comprehensive information

4. **Monitor Activity:**
   - Check Dashboard for overview metrics
   - Review Action Log for audit trail

### For System Administrators:

1. **Monitor Platform Health:**
   - Check tenant distribution
   - Monitor revenue trends
   - Track usage patterns

2. **Manage Subscriptions:**
   - Upgrade/downgrade tenant plans
   - Suspend non-paying tenants
   - Grant trial extensions

3. **Audit Actions:**
   - Review all administrative changes
   - Track who made what changes
   - Ensure compliance

## API Response Examples

### Dashboard Response:
```json
{
  "tenants": {
    "total": 150,
    "active": 120,
    "trial": 20,
    "suspended": 10
  },
  "plans": {
    "free": 80,
    "startup": 40,
    "professional": 25,
    "enterprise": 5
  },
  "revenue": {
    "mrr": 789955,
    "currency": "INR"
  },
  "growth": {
    "recent_signups_30d": 25
  },
  "users": {
    "total": 450
  },
  "usage": {
    "current_month": "2024-11",
    "total_ai_credits_used": 15000,
    "total_tokens_consumed": 5000000,
    "total_cost_incurred": 12500.50
  }
}
```

### Tenant List Response:
```json
{
  "tenants": [
    {
      "id": "tenant_123",
      "name": "Acme Corp",
      "plan": "professional",
      "status": "active",
      "member_count": 5,
      "created_at": "2024-10-15T10:30:00Z",
      "current_usage": {
        "ai_credits_used": 500,
        "ai_tokens_consumed": 150000,
        "cost_incurred": 450.00
      }
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 150,
    "totalPages": 3
  }
}
```

## Troubleshooting

### Access Denied (403 Error):
- Verify user email ends with @hexabid.com
- Or add user ID to SUPER_ADMIN_IDS list
- Restart backend after changes

### Data Not Loading:
- Check backend is running: `sudo supervisorctl status backend`
- Verify MongoDB connection
- Check browser console for errors

### Actions Not Being Logged:
- Verify admin_actions collection exists
- Check database permissions
- Review backend logs

## Future Enhancements

Planned features:
- [ ] Advanced filtering and search
- [ ] Export tenant data to CSV
- [ ] Bulk tenant operations
- [ ] Custom role management
- [ ] Email notifications for critical events
- [ ] Advanced analytics dashboard
- [ ] Tenant usage forecasting
- [ ] Automated billing reminders

---

**Version:** 1.0
**Last Updated:** November 2024
**Status:** ✅ Fully Implemented and Operational
