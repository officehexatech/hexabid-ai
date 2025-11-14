# 🚀 HexaBid - 60 Second Quick Start

## ONE COMMAND LAUNCH

```bash
cd /app && chmod +x launch.sh && ./launch.sh
```

That's it! The application will:
1. ✅ Check prerequisites
2. ✅ Start PostgreSQL & Redis (Docker)
3. ✅ Build backend (zero errors)
4. ✅ Build frontend (zero errors)
5. ✅ Start both servers
6. ✅ Open automatically

---

## MANUAL START (3 Commands)

### Terminal 1: Infrastructure
```bash
docker-compose up -d
```

### Terminal 2: Backend
```bash
cd backend-nestjs && npm run start:dev
```

### Terminal 3: Frontend
```bash
cd frontend-react && npm start
```

---

## TEST LOGIN

1. **Open**: http://localhost:3001
2. **Email**: test@example.com (any email works)
3. **Click**: "Send OTP"
4. **Check**: Backend terminal for OTP
5. **Enter**: 6-digit OTP
6. **Login**: You're in!

---

## VERIFY IT WORKS

✅ Backend: http://localhost:3000/api/docs
✅ Frontend: http://localhost:3001
✅ Login works
✅ Dashboard loads
✅ Tenders page works

---

## TROUBLESHOOTING

**Port conflict?**
```bash
kill $(lsof -ti:3000,3001)
```

**Database issue?**
```bash
docker-compose restart postgres
```

**Start fresh?**
```bash
docker-compose down -v
docker-compose up -d
```

---

## STOP EVERYTHING

```bash
# Stop backend & frontend (Ctrl+C in terminals)
# Stop infrastructure
docker-compose down
```

---

**That's it! Error-free and ready to go! 🎉**
