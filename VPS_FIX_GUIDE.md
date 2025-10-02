# 🔧 VPS MongoDB Connection Fix Guide

## 🎯 Problem Identified

**Issue:** API container trying to connect to `mirai-mongodb:27017` but actual container name is `mongodb`

**Network Status:**
```
Network: cloudflared (172.21.0.0/16)
├── mongodb (172.21.0.7)          ← Actual name
├── mirai-pixel-api (172.21.0.3)  ← Trying to connect to "mirai-mongodb"
├── redis (172.21.0.6)
├── postgresql (172.21.0.5)
├── cloudflared (172.21.0.4)
└── portainer (172.21.0.2)
```

**Error:**
```
mirai-mongodb:27017: [Errno -3] Temporary failure in name resolution
```

---

## ✅ Solution

Change MongoDB URI from `mongodb://mirai-mongodb:27017/` to `mongodb://mongodb:27017/`

---

## 🚀 Quick Fix (Run on VPS)

### Option 1: Automatic Fix Script

```bash
cd ~/workspace/image-generator

# Create fix script
cat > fix_mongodb.sh << 'SCRIPT'
#!/bin/bash
echo "🔧 Fixing MongoDB connection..."

# Update docker-compose.yml
sed -i 's|mongodb://mirai-mongodb:27017/|mongodb://mongodb:27017/|g' docker-compose.yml

# Recreate container
docker compose up -d --force-recreate pixel-api

# Wait and test
sleep 5
echo "🧪 Testing..."
curl -s http://localhost:8000/api/histories?limit=1 | python3 -m json.tool | head -20

echo "✅ Done!"
SCRIPT

chmod +x fix_mongodb.sh
./fix_mongodb.sh
```

### Option 2: Manual Fix

**Step 1: Edit docker-compose.yml**

```bash
cd ~/workspace/image-generator
nano docker-compose.yml
```

Change this line:
```yaml
- MONGODB_URI=mongodb://mirai-mongodb:27017/
```

To:
```yaml
- MONGODB_URI=mongodb://mongodb:27017/
```

**Step 2: Recreate container**

```bash
docker compose up -d --force-recreate pixel-api
```

**Step 3: Verify**

```bash
# Check logs
docker logs mirai-pixel-api --tail 20

# Test API
curl http://localhost:8000/api/histories?limit=1
```

---

## 🧪 Verification

After fix, you should see:

```bash
$ curl http://localhost:8000/api/histories?limit=1
{
  "success": true,
  "timestamp": "2025-10-02T09:30:00.000000",
  "message": "Retrieved 1 histories",
  "data": {
    "items": [...]
  }
}
```

**Logs should show:**
```
INFO:     Started server process [1]
INFO:     Application startup complete.
🚀 Starting Mirai Puzzle API...
📦 Version: 2.0.0
🗄️  MongoDB: mongodb://mongodb:27017/
💾 Database: Mirai_Puzzle
INFO:     172.21.0.4:49222 - "GET /api/histories HTTP/1.1" 200 OK
```

---

## 📝 Updated docker-compose.yml

```yaml
services:
  # API Service
  pixel-api:
    build: .
    container_name: mirai-pixel-api
    restart: unless-stopped
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/      # ✅ Fixed
      - MONGODB_DATABASE=Mirai_Puzzle
    networks:
      - cloudflared
    expose:
      - "8000"

networks:
  cloudflared:
    external: true
    name: cloudflared
```

---

## 🔍 Troubleshooting

### If still failing:

**1. Check MongoDB is running:**
```bash
docker ps | grep mongodb
# Should show: mongodb   Up X hours
```

**2. Check network connectivity:**
```bash
docker exec mirai-pixel-api ping -c 2 mongodb
# Should show: 2 packets transmitted, 2 received
```

**3. Check MongoDB port:**
```bash
docker exec mongodb netstat -tln | grep 27017
# Should show: tcp        0      0 0.0.0.0:27017
```

**4. Test MongoDB directly:**
```bash
docker exec mongodb mongosh --eval "db.adminCommand('ping')"
# Should show: { ok: 1 }
```

**5. Check API environment:**
```bash
docker exec mirai-pixel-api env | grep MONGODB
# Should show:
# MONGODB_URI=mongodb://mongodb:27017/
# MONGODB_DATABASE=Mirai_Puzzle
```

---

## 💡 Alternative Solutions

### Solution A: Create Network Alias

Keep config as `mirai-mongodb` and create alias:

```bash
docker network disconnect cloudflared mongodb
docker network connect cloudflared mongodb --alias mirai-mongodb
docker restart mirai-pixel-api
```

### Solution B: Use IP Address

Use direct IP instead of hostname:

```yaml
environment:
  - MONGODB_URI=mongodb://172.21.0.7:27017/
```

---

## 🎯 Summary

**Root Cause:** Container name mismatch
- Config expects: `mirai-mongodb`
- Actual name: `mongodb`

**Fix:** Update `MONGODB_URI` to use correct container name

**Files Changed:**
- `docker-compose.yml` (line 7)

**Commands:**
```bash
# Fix
sed -i 's|mirai-mongodb|mongodb|g' docker-compose.yml
docker compose up -d --force-recreate pixel-api

# Verify
curl http://localhost:8000/api/histories?limit=1
```

---

## ✅ Checklist

- [ ] Updated docker-compose.yml
- [ ] Recreated container
- [ ] Checked logs (no errors)
- [ ] Tested API endpoint
- [ ] Verified MongoDB connection
- [ ] Committed changes to git

---

**After fix, API should work perfectly!** 🚀

