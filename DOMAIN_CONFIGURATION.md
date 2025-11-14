# HexaBid Domain Configuration Guide
## Domain: hexabid.co.in

---

## 🎯 Overview
This guide will help you configure your custom domain **hexabid.co.in** for the HexaBid platform.

---

## 📋 Prerequisites
1. Access to your domain registrar's DNS management panel
2. Current preview URL: `https://bid-manage-hub.preview.emergentagent.com`
3. Domain: `hexabid.co.in`

---

## 🌐 DNS Configuration

### Step 1: Access Your Domain Registrar
Log into your domain registrar's control panel where you purchased `hexabid.co.in` (e.g., GoDaddy, Namecheap, etc.)

### Step 2: Configure DNS Records

Add the following DNS records:

#### A Record (Primary Domain)
```
Type: A
Name: @ (or leave blank for root domain)
Value: [IP Address of Emergent Server]
TTL: 3600 (or Auto)
```

#### CNAME Record (WWW Subdomain)
```
Type: CNAME
Name: www
Value: tender-master-4.preview.emergentagent.com
TTL: 3600 (or Auto)
```

**Alternative CNAME Approach:**
If your registrar supports CNAME flattening:
```
Type: CNAME
Name: @ (or hexabid.co.in)
Value: tender-master-4.preview.emergentagent.com
TTL: 3600 (or Auto)
```

---

## ⚙️ Application Configuration

### Backend Configuration (.env)

Update `/app/backend/.env`:
```env
# Add allowed origins
CORS_ORIGINS="https://hexabid.co.in,https://www.hexabid.co.in,http://hexabid.co.in"

# Add domain to JWT secret context (optional)
DOMAIN="hexabid.co.in"

# Keep existing settings
MONGO_URL="mongodb://localhost:27017"
DB_NAME="test_database"
EMERGENT_LLM_KEY=sk-emergent-6909dD1Ad8eD016450
JWT_SECRET=hexabid-secret-key-change-this
```

### Frontend Configuration (.env)

Update `/app/frontend/.env`:
```env
# Update backend URL for production
REACT_APP_BACKEND_URL=https://hexabid.co.in

# Other settings
PORT=443
REACT_APP_ENABLE_VISUAL_EDITS=false
ENABLE_HEALTH_CHECK=false
```

---

## 🔒 SSL/HTTPS Configuration

### Option 1: Emergent Platform (Recommended)
If using Emergent's infrastructure:
1. SSL certificates are automatically provisioned
2. HTTPS is enabled by default
3. No manual configuration needed

### Option 2: Let's Encrypt (Self-Hosted)
If self-hosting:
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL Certificate
sudo certbot --nginx -d hexabid.co.in -d www.hexabid.co.in

# Auto-renewal is configured automatically
```

---

## 🔄 After DNS Configuration

### 1. DNS Propagation
- DNS changes can take 1-48 hours to propagate globally
- Check propagation status: https://dnschecker.org
- Enter: `hexabid.co.in`

### 2. Verify Configuration

Test the domain:
```bash
# Check DNS resolution
dig hexabid.co.in
nslookup hexabid.co.in

# Test HTTP/HTTPS
curl -I https://hexabid.co.in
curl -I https://www.hexabid.co.in
```

### 3. Clear Browser Cache
```
Chrome: Ctrl + Shift + Delete
Firefox: Ctrl + Shift + Delete
Safari: Cmd + Option + E
```

### 4. Test All Features
- [ ] Landing page loads
- [ ] Registration works
- [ ] Login works
- [ ] Dashboard accessible
- [ ] AI Chatbot functions
- [ ] WhatsApp button opens correctly
- [ ] All API endpoints work

---

## 🔧 Troubleshooting

### Issue: "Site Can't Be Reached"
**Solution:**
1. Verify DNS records are correct
2. Wait for DNS propagation (24-48 hours)
3. Check domain is not parked or suspended
4. Verify nameservers are configured correctly

### Issue: "CORS Error" in Browser
**Solution:**
1. Ensure CORS_ORIGINS in backend .env includes your domain
2. Restart backend: `sudo supervisorctl restart backend`
3. Clear browser cache

### Issue: "Mixed Content" Warnings
**Solution:**
1. Ensure all resources use HTTPS
2. Update API URL to use HTTPS
3. Check for hardcoded HTTP URLs

### Issue: SSL Certificate Error
**Solution:**
1. Verify SSL certificate is installed
2. Check certificate validity period
3. Ensure certificate covers both `hexabid.co.in` and `www.hexabid.co.in`

---

## 📊 Post-Configuration Checklist

### DNS Configuration
- [ ] A record configured for root domain
- [ ] CNAME record configured for www subdomain
- [ ] DNS propagation verified
- [ ] Domain resolves correctly

### Application Configuration
- [ ] Backend CORS updated
- [ ] Frontend API URL updated
- [ ] Services restarted
- [ ] All environment variables correct

### SSL/Security
- [ ] HTTPS working
- [ ] SSL certificate valid
- [ ] No mixed content warnings
- [ ] Secure cookies configured

### Functionality Testing
- [ ] Landing page loads correctly
- [ ] User registration works
- [ ] Login/logout functions
- [ ] Google OAuth works
- [ ] All dashboard features accessible
- [ ] AI Chatbot responds
- [ ] WhatsApp button redirects correctly
- [ ] Email verification (if configured)

---

## 🚀 Going Live Commands

Once DNS is configured and propagated:

```bash
# 1. Update environment variables
cd /app/backend
nano .env  # Update CORS_ORIGINS

cd /app/frontend
nano .env  # Update REACT_APP_BACKEND_URL

# 2. Restart all services
sudo supervisorctl restart all

# 3. Verify services are running
sudo supervisorctl status

# 4. Check logs
tail -f /var/log/supervisor/backend.err.log
tail -f /var/log/supervisor/frontend.err.log

# 5. Test the application
curl -I https://hexabid.co.in
curl https://hexabid.co.in/api/health
```

---

## 📞 Support Contact

If you need assistance with domain configuration:

**HexaBid Support:**
- Email: support@cctverp.com
- Phone: +91 8806106575, +91 9607500750
- WhatsApp: +91 8806106575

**Emergent Platform Support:**
- Documentation: https://docs.emergentagent.com
- Support: support@emergentagent.com

---

## 🎉 Success!

Once configured, your HexaBid platform will be accessible at:
- **Primary:** https://hexabid.co.in
- **Alternative:** https://www.hexabid.co.in

All users, vendors, and data will be preserved during the domain transition.

---

**Created by Snxwfairies Innovations Pvt. Ltd.**
**Powered by HexaBid Platform**