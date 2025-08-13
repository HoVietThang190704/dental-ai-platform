# Dental AI Platform

Nền tảng AI cho phân tích và mô phỏng nha khoa với các dịch vụ microservices.

## 📋 Mục lục

- [Tổng quan](#tổng-quan)
- [Kiến trúc hệ thống](#kiến-trúc-hệ-thống)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt và chạy dự án](#cài-đặt-và-chạy-dự-án)
- [Cấu hình môi trường](#cấu-hình-môi-trường)
- [Sử dụng](#sử-dụng)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## 🎯 Tổng quan

Dental AI Platform là một hệ thống phân tích và mô phỏng nha khoa sử dụng AI, bao gồm:

- **Frontend**: Giao diện người dùng React + TypeScript + Vite
- **Gateway**: API Gateway với Node.js + TypeScript + Prisma
- **AI Service**: Dịch vụ AI với Python + FastAPI
- **Database**: PostgreSQL cho lưu trữ dữ liệu
- **Storage**: MinIO cho lưu trữ file
- **Cache**: Redis cho caching

## 🏗️ Kiến trúc hệ thống

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Frontend  │────│   Gateway   │────│ AI Service  │
│ (React/TS)  │    │ (Node.js)   │    │ (FastAPI)   │
└─────────────┘    └─────────────┘    └─────────────┘
                           │
                   ┌───────┼───────┐
                   │       │       │
            ┌─────────┐ ┌─────┐ ┌─────────┐
            │PostgreSQL│ │Redis│ │  MinIO  │
            │    DB   │ │Cache│ │ Storage │
            └─────────┘ └─────┘ └─────────┘
```

## 💻 Yêu cầu hệ thống

### Phần mềm bắt buộc:
- **Docker** và **Docker Compose** (phiên bản mới nhất)
- **Node.js** v18+ (để phát triển)
- **Python** 3.9+ (để phát triển AI service)
- **Git**

### Hệ điều hành:
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

## 🚀 Cài đặt và chạy dự án

### Bước 1: Clone repository

```bash
git clone https://github.com/HoVietThang190704/dental-ai-platform.git
cd dental-ai-platform
```

### Bước 2: Cấu hình môi trường

Tạo các file môi trường từ template:

```bash
# Tạo file .env chính
cp .env.example .env

# Tạo file .env cho gateway
cp gateway/.env.example gateway/.env

# Tạo file .env cho ai-service
cp ai-service/.env.example ai-service/.env
```

### Bước 3: Cấu hình file .env

Chỉnh sửa file `.env` trong thư mục root:

```env
# Database
POSTGRES_DB=dental_ai_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_secure_password

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123
S3_BUCKET=dental-uploads

# Redis (không cần cấu hình thêm)
```

### Bước 4: Chạy dự án với Docker

```bash
# Chạy tất cả các service
docker-compose up -d

# Xem logs
docker-compose logs -f

# Chỉ chạy một số service cụ thể
docker-compose up -d db redis minio
```

### Bước 5: Chạy database migrations

```bash
# Vào thư mục gateway
cd gateway

# Chạy Prisma migrations
npm run prisma:migrate

# Generate Prisma client
npm run prisma:generate
```

## ⚙️ Cấu hình môi trường

### Gateway (.env)

```env
# Database
DATABASE_URL="postgresql://postgres:your_secure_password@localhost:5432/dental_ai_platform"

# Redis
REDIS_URL="redis://localhost:6379"

# MinIO
MINIO_ENDPOINT="localhost"
MINIO_PORT=9000
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin123"
MINIO_BUCKET_NAME="dental-uploads"

# AI Service
AI_SERVICE_URL="http://localhost:8000"

# Server
PORT=3000
NODE_ENV=development
```

### AI Service (.env)

```env
# FastAPI
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Database connection (nếu cần)
DATABASE_URL="postgresql://postgres:your_secure_password@localhost:5432/dental_ai_platform"
```

## 🔧 Development Mode

### Chạy từng service riêng biệt:

#### 1. Database & Infrastructure
```bash
docker-compose up -d db redis minio createbuckets
```

#### 2. Gateway
```bash
cd gateway
npm install
npm run dev
```

#### 3. AI Service
```bash
cd ai-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🌐 Sử dụng

Sau khi chạy thành công, bạn có thể truy cập:

- **Frontend**: http://localhost:5173
- **Gateway API**: http://localhost:3000
- **AI Service**: http://localhost:8000
- **AI Service Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001
- **PostgreSQL**: localhost:5432

## 📚 API Documentation

### Gateway Endpoints:

```
GET    /api/health              # Health check
POST   /api/uploads             # Upload files
GET    /api/analysis            # Get analysis results
POST   /api/analysis            # Create new analysis
GET    /api/chat/history        # Get chat history
POST   /api/chat/message        # Send chat message
GET    /api/simulations         # Get simulations
POST   /api/simulations         # Create simulation
```

### AI Service Endpoints:

```
GET    /                        # Health check
POST   /api/analysis            # AI Analysis
POST   /api/chat                # AI Chat
POST   /api/simulation          # AI Simulation
GET    /docs                    # Swagger documentation
```

## 🔍 Troubleshooting

### Lỗi thường gặp:

#### 1. Container không khởi động được
```bash
# Kiểm tra logs
docker-compose logs [service_name]

# Restart services
docker-compose down
docker-compose up -d
```

#### 2. Database connection failed
```bash
# Kiểm tra PostgreSQL container
docker-compose ps db

# Reset database
docker-compose down -v
docker-compose up -d
```

#### 3. Prisma migration failed
```bash
cd gateway
npm run prisma:generate
npm run prisma:migrate
```

#### 4. Port bị chiếm
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/macOS
lsof -ti:3000 | xargs kill -9
```

#### 5. MinIO bucket không tạo được
```bash
# Restart MinIO services
docker-compose restart minio createbuckets
```

### Làm sạch dự án:

```bash
# Dừng tất cả containers
docker-compose down

# Xóa volumes (sẽ mất dữ liệu)
docker-compose down -v

# Xóa images
docker-compose down --rmi all

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## 🛠️ Scripts hữu ích

### Backup database:
```bash
docker exec -t dental-ai-platform_db_1 pg_dump -c -U postgres dental_ai_platform > backup.sql
```

### Restore database:
```bash
cat backup.sql | docker exec -i dental-ai-platform_db_1 psql -U postgres -d dental_ai_platform
```

### Reset project:
```bash
# Script để reset toàn bộ project
./scripts/reset.sh  # Linux/macOS
./scripts/reset.bat # Windows
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:

1. Kiểm tra [Issues](https://github.com/HoVietThang190704/dental-ai-platform/issues)
2. Tạo issue mới với thông tin chi tiết
3. Liên hệ team phát triển

---

**Phát triển bởi**: Dental AI Platform Team  
**Phiên bản**: 1.0.0  
**Cập nhật**: August 2025