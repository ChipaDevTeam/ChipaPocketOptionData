# Template Usage Guide

This document provides step-by-step instructions for using this template to create new projects.

## 🎯 Overview

This template provides a complete, production-ready setup for containerized applications with:
- ✅ Docker multi-stage builds
- ✅ Local development with Docker Compose
- ✅ Automated deployment to Google Cloud Run
- ✅ Configuration management
- ✅ Environment variable handling
- ✅ CI/CD ready structure

## 🚀 Getting Started

### Step 1: Clone or Download the Template

```bash
# Option 1: Clone (if this is a Git repository)
git clone <repository-url> my-new-project
cd my-new-project

# Option 2: Download and extract
# Then cd into the directory
```

### Step 2: Run the Setup Script

The interactive setup script will configure the template for your project:

```bash
./setup.sh
```

You'll be prompted for:
- **Project name**: lowercase, no spaces (e.g., `my-awesome-api`)
- **Display name**: Human-readable (e.g., `My Awesome API`)
- **Description**: Brief project description
- **Port**: Service port (default: 8080)
- **Docker image name**: Container image name
- **GCP Project ID**: (optional) Your Google Cloud project
- **Region**: GCP region (default: us-central1)
- **Binary name**: Name of your compiled executable

The script will automatically:
- Update `project.config.json` with your settings
- Create `.env` from `.env.example`
- Update `README.md` title

### Step 3: Customize for Your Tech Stack

#### For Node.js/TypeScript Projects

1. **Update Dockerfile**:
```dockerfile
# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
EXPOSE 8080
CMD ["node", "dist/index.js"]
```

2. **Add your package.json** and source code

3. **Update docker-compose.yml** if needed:
```yaml
volumes:
  - ./src:/app/src:ro  # For development hot-reload
```

#### For Python Projects

1. **Update Dockerfile**:
```dockerfile
# Builder stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /app /app
EXPOSE 8080
CMD ["python", "main.py"]
```

2. **Add requirements.txt** and your Python code

#### For Go Projects

1. **Update Dockerfile**:
```dockerfile
# Builder stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o server

# Runtime stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=builder /app/server .
EXPOSE 8080
CMD ["./server"]
```

#### For Rust Projects

1. **Update Dockerfile**:
```dockerfile
# Builder stage
FROM rust:slim-bookworm AS builder
WORKDIR /app
COPY Cargo.* ./
COPY src ./src
RUN cargo build --release

# Runtime stage
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /app/target/release/your-binary .
EXPOSE 8080
CMD ["./your-binary"]
```

### Step 4: Add Your Application Code

1. Create your source directory:
```bash
mkdir -p src
# Add your application files
```

2. Update the Dockerfile `COPY` commands to include your code

3. Ensure your app reads configuration from environment variables:
   - `PORT` - Server port
   - `LOG_LEVEL` - Logging level
   - `DATABASE_URL` - Database connection string (if needed)
   - Add custom variables to `.env`

### Step 5: Configure Environment Variables

1. Edit `.env` with your specific values:
```bash
# Essential settings
PROJECT_NAME=my-project
PORT=8080
LOG_LEVEL=info

# Add your service URLs
API_BASE_URL=https://api.example.com
DATABASE_URL=postgresql://user:pass@host:5432/db

# GCP settings
GCP_PROJECT_ID=your-project-id
REGION=us-central1
```

2. Update `project.config.json` for advanced configuration:
```json
{
  "project": {
    "name": "my-project",
    "displayName": "My Project"
  },
  "gcp": {
    "cloudRun": {
      "memory": "2Gi",
      "cpu": "2",
      "maxInstances": "10"
    }
  }
}
```

### Step 6: Test Locally

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or just start services
docker-compose up

# Test your API
curl http://localhost:8080/health

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 7: Deploy to Production

#### First-time Setup

1. **Install gcloud CLI**: https://cloud.google.com/sdk/docs/install

2. **Authenticate**:
```bash
gcloud auth login
gcloud auth configure-docker
```

3. **Create GCP Project** (if needed):
```bash
gcloud projects create YOUR-PROJECT-ID
gcloud config set project YOUR-PROJECT-ID
```

4. **Enable billing** for your project in the GCP Console

#### Deploy

```bash
# Simple deployment
./deploy.sh

# Or with explicit project
GCP_PROJECT_ID=your-project ./deploy.sh

# Use Cloud Build instead of local build
USE_LOCAL_BUILD=false ./deploy.sh
```

The script will:
- ✅ Enable required GCP APIs
- ✅ Build your Docker image
- ✅ Push to Google Container Registry
- ✅ Deploy to Cloud Run
- ✅ Provide your service URL

### Step 8: Configure CI/CD (Optional)

#### GitHub Actions

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - name: Deploy
        run: |
          gcloud builds submit --config cloudbuild.yaml
```

## 📋 Checklist

Before deploying:
- [ ] Run `./setup.sh` to initialize configuration
- [ ] Customize `Dockerfile` for your tech stack
- [ ] Add your application code
- [ ] Update `.env` with your settings
- [ ] Test locally with `docker-compose up`
- [ ] Update `README.md` with project-specific info
- [ ] Set up GCP project and enable billing
- [ ] Run `./deploy.sh` to deploy

## 🎓 Examples

### Adding a Database

Edit `docker-compose.yml`:
```yaml
services:
  api:
    # ... existing config
    depends_on:
      - postgres
    environment:
      - DATABASE_URL=postgresql://postgres:password@postgres:5432/mydb

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
```

### Adding Redis Cache

```yaml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data

volumes:
  redis-data:
```

### Environment-Specific Configuration

Update `project.config.json`:
```json
{
  "environment": {
    "production": {
      "LOG_LEVEL": "warn",
      "API_BASE_URL": "https://api.prod.com",
      "ENABLE_METRICS": true
    },
    "staging": {
      "LOG_LEVEL": "info",
      "API_BASE_URL": "https://api.staging.com",
      "ENABLE_METRICS": true
    },
    "development": {
      "LOG_LEVEL": "debug",
      "API_BASE_URL": "http://localhost:8080",
      "ENABLE_METRICS": false
    }
  }
}
```

## 🆘 Need Help?

- Check `README.md` for detailed documentation
- Review example Dockerfiles in comments
- Check GCP documentation: https://cloud.google.com/run/docs
- Review Docker best practices: https://docs.docker.com/develop/dev-best-practices/

## 🎉 You're Ready!

Your template is now configured and ready to use. Happy coding! 🚀
