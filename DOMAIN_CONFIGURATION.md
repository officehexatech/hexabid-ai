# HexaBid - Domain Configuration

## 🌐 Custom Domains

### Primary Domain
**https://hexabid.in/**
- Main production domain
- All API calls configured to use this domain
- Backend accessible at: `https://hexabid.in/api/*`

### Secondary Domain
**https://hexabid.info/**
- Alternative domain (mirror/backup)
- Can be used for regional access or marketing
- Backend accessible at: `https://hexabid.info/api/*`

### Preview Domain (Development)
**https://hexabid.preview.emergentagent.com/**
- Emergent platform preview domain
- Used for testing and development
- Backend accessible at: `https://hexabid.preview.emergentagent.com/api/*`

## 📝 Configuration Status

### Frontend Configuration
- **File**: `/app/frontend/.env`
- **Backend URL**: `https://hexabid.in`
- All API calls use this base URL + `/api` prefix

### Backend Configuration
- **File**: `/app/backend/.env`
- **CORS Origins**: Configured to allow all three domains
  - `https://hexabid.in`
  - `https://hexabid.info`
  - `https://hexabid.preview.emergentagent.com`

### API Endpoints Structure
All backend routes are prefixed with `/api/`:
- Authentication: `/api/auth/*`
- Tenders: `/api/tenders/*`
- AI Agents: `/api/ai-agents/*`
- GeM Portal: `/api/gem/*`
- CPP Portal: `/api/cpp/*`
- Search: `/api/search/*`
- Competitors: `/api/competitors/*`
- Buyers: `/api/buyers/*`
- PDF Tools: `/api/pdf-tools/*`
- Email: `/api/email/*`
- Office 365: `/api/office365/*`

## 🔒 Security Configuration

### CORS (Cross-Origin Resource Sharing)
- Configured in backend to accept requests from all three domains
- Credentials enabled for authenticated requests
- Proper origin validation in place

### HTTPS/SSL
- All domains use HTTPS
- SSL certificates managed by Emergent platform
- Secure WebSocket connections enabled

## 🚀 Deployment Notes

### DNS Configuration Required
To make the custom domains work, you need to configure DNS records:

**For hexabid.in:**
```
Type: CNAME or A Record
Host: @ (or hexabid.in)
Value: [Emergent platform IP/CNAME provided by support]
```

**For hexabid.info:**
```
Type: CNAME or A Record
Host: @ (or hexabid.info)
Value: [Emergent platform IP/CNAME provided by support]
```

**For www subdomains (optional):**
```
Type: CNAME
Host: www
Value: hexabid.in (or hexabid.info)
```

### Steps to Enable Custom Domains on Emergent:
1. Contact Emergent support to add custom domains
2. Provide domain names: `hexabid.in` and `hexabid.info`
3. Update DNS records at your domain registrar
4. Wait for DNS propagation (24-48 hours)
5. Emergent will provision SSL certificates
6. Verify domains are accessible

## 📊 Current Status

✅ Frontend configured to use `hexabid.in`
✅ Backend CORS configured for all domains
✅ Environment variables updated
✅ Services restarted with new configuration
⏳ Awaiting DNS configuration and Emergent domain setup

## 🔗 Access URLs

Once DNS is configured, access the application at:
- **Primary**: https://hexabid.in
- **Secondary**: https://hexabid.info
- **Preview**: https://hexabid.preview.emergentagent.com (already working)

## 📞 Support

For domain setup on Emergent platform:
- Contact Emergent support team
- Provide this document for reference
- Request custom domain activation for HexaBid app

---

**Last Updated**: November 2024
**Configuration Version**: 1.0
**App Name**: HexaBid - AI-Powered Tender Automation Platform
