# 🔄 Migration Guide: v1.0 → v2.0

## 📋 Tóm tắt thay đổi

### ✅ Đã hoàn thành:

1. **Tái cấu trúc dự án theo module**
   - Tách code thành các module rõ ràng
   - Dễ dàng maintain và mở rộng

2. **Module Image Converter** (`/image`)
   - Chuyển đổi ảnh thành pixel art
   - Chỉ trả về màu thực sự có trong ảnh
   - Bỏ chức năng `palette_override` (tránh sai hình)

3. **Module Database** (`/db`)
   - Quản lý MongoDB với 3 collections: images, histories, imports
   - CRUD operations đầy đủ
   - Async/await với Motor driver

4. **Configuration Management**
   - Centralized config trong `app/config.py`
   - Hỗ trợ `.env` file
   - Pydantic settings validation

5. **Docker Setup**
   - MongoDB container
   - API container
   - Docker Compose orchestration

## 📁 Cấu trúc mới

```
ImageGenPython/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app chính
│   ├── config.py               # Configuration
│   ├── modules/
│   │   ├── image_converter/    # Module gen ảnh
│   │   │   ├── routes.py
│   │   │   ├── service.py
│   │   │   └── utils.py
│   │   └── database/           # Module MongoDB
│   │       ├── routes.py
│   │       ├── service.py
│   │       ├── models.py
│   │       └── connection.py
│   └── utils/
│       └── helpers.py          # Common helpers
├── tests/                      # Test files
├── requirements.txt
├── docker-compose.yml
└── Dockerfile
```

## 🔄 API Changes

### Image Converter

#### Before (v1.0):
```
GET /palette
POST /convert
```

#### After (v2.0):
```
GET /image/palette
POST /image/convert
```

**Breaking Changes:**
- ❌ Removed: `palette_override` parameter
- ✅ Changed: Response chỉ chứa màu thực sự có trong ảnh

### Database (NEW in v2.0)

```
# Images
POST   /db/images
GET    /db/images
GET    /db/images/{id}
PUT    /db/images/{id}
DELETE /db/images/{id}

# Histories
POST   /db/histories
GET    /db/histories

# Imports
POST   /db/imports
GET    /db/imports
GET    /db/imports/{id}
PUT    /db/imports/{id}/status
```

## 🚀 Deployment

### Development

```bash
# Chạy với Docker
docker compose up --build

# Hoặc chạy local
python -m app.main
```

### Production

1. Update `.env` với production values
2. Build và deploy:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing

```bash
# Test API
./tests/test_api.sh

# Test với curl
curl http://localhost:8000
curl http://localhost:8000/image/palette
```

## 📝 Migration Checklist

- [ ] Update client code để sử dụng endpoints mới
- [ ] Remove `palette_override` logic từ client
- [ ] Test image conversion với API mới
- [ ] Setup MongoDB connection
- [ ] Migrate existing data (nếu có)
- [ ] Update documentation
- [ ] Update CI/CD pipeline

## 🔧 Configuration

### Environment Variables

```bash
# .env
MONGODB_URI=mongodb://mongodb:27017/
MONGODB_DATABASE=Mirai_Puzzle
DEBUG=true
```

### Docker Compose

```yaml
services:
  mongodb:
    image: mongo:7.0
    # ...
  
  pixel-api:
    build: .
    depends_on:
      - mongodb
    environment:
      - MONGODB_URI=mongodb://mongodb:27017/
```

## 🐛 Troubleshooting

### API không response

```bash
# Kiểm tra logs
docker compose logs pixel-api

# Kiểm tra network
docker network inspect cloudflared

# Restart services
docker compose restart
```

### MongoDB connection error

```bash
# Kiểm tra MongoDB
docker compose logs mongodb

# Test connection
docker exec -it mirai-mongodb mongosh
```

### Port conflict

```bash
# Tìm process đang dùng port
lsof -i :8000
lsof -i :27017

# Kill process
kill -9 <PID>
```

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 💡 Next Steps

1. **Add Authentication**: JWT tokens, OAuth2
2. **Add Caching**: Redis for frequently accessed data
3. **Add Queue**: Celery for background tasks
4. **Add Monitoring**: Prometheus, Grafana
5. **Add Logging**: Structured logging with ELK stack
6. **Add Tests**: Unit tests, integration tests
7. **Add CI/CD**: GitHub Actions, GitLab CI

## 🎯 Benefits of v2.0

1. **Modular Architecture**: Dễ maintain và mở rộng
2. **Database Integration**: Lưu trữ và quản lý dữ liệu
3. **Better Organization**: Code structure rõ ràng
4. **Scalability**: Dễ dàng thêm module mới
5. **Type Safety**: Pydantic models validation
6. **Async Support**: Better performance với async/await
7. **Docker Ready**: Easy deployment với Docker

## ✨ Conclusion

Version 2.0 mang lại kiến trúc tốt hơn, dễ maintain hơn và sẵn sàng cho production. Tất cả các thay đổi đều hướng tới việc tạo ra một API robust, scalable và dễ sử dụng.

