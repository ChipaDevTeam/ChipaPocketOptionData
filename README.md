# Project Template

A production-ready template for containerized applications with automated deployment to Google Cloud Run.

## 🚀 Quick Start

### 1. Initialize Your Project

Run the setup script to customize this template for your project:

```bash
./setup.sh
```

This interactive script will guide you through configuring:
- Project name and description
- Docker container settings
- GCP deployment configuration
- Service ports and endpoints

### 2. Configure Your Application

After running setup, edit the following files as needed:

#### `project.config.json`
Central configuration file containing all project settings:
- Project metadata (name, description, version)
- Docker configuration (image name, ports, directories)
- Build settings (commands, binary names, platforms)
- GCP settings (project ID, region, Cloud Run configuration)
- Environment-specific settings (production, staging, development)

#### `.env`
Environment variables for your application (created from `.env.example`):
- Server configuration (port, logging)
- External service URLs (APIs, databases)
- Cloud storage settings
- Feature flags

#### `Dockerfile`
Customize the build process for your technology stack:
- Update base images for your language/framework
- Add build dependencies
- Configure build commands
- Copy artifacts to runtime image

### 3. Local Development

#### Using Docker Compose

```bash
# Start all services
docker-compose up

# Build and start in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Environment Variables

Create a `.env` file from the template:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Deploy to Production

#### Prerequisites
- [Docker](https://www.docker.com/products/docker-desktop) (for local builds)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)
- GCP project with billing enabled

#### Deploy Script

```bash
# Deploy using local Docker build (faster for small projects)
./deploy.sh

# Or use Cloud Build (better for complex builds)
USE_LOCAL_BUILD=false ./deploy.sh

# Override GCP project
GCP_PROJECT_ID=my-project ./deploy.sh
```

The deploy script will:
1. Read configuration from `project.config.json`
2. Enable required GCP APIs
3. Build Docker image (locally or via Cloud Build)
4. Push to Google Container Registry
5. Deploy to Cloud Run
6. Provide service URL and testing commands

#### Manual Deployment

```bash
# Set your GCP project
gcloud config set project YOUR_PROJECT_ID

# Build and push manually
docker build -t gcr.io/YOUR_PROJECT_ID/SERVICE_NAME:latest .
docker push gcr.io/YOUR_PROJECT_ID/SERVICE_NAME:latest

# Deploy to Cloud Run
gcloud run deploy SERVICE_NAME \
  --image gcr.io/YOUR_PROJECT_ID/SERVICE_NAME:latest \
  --region us-central1 \
  --platform managed
```

## 📁 Project Structure

```
.
├── project.config.json      # Central project configuration
├── .env.example             # Environment variable template
├── .env                     # Your environment variables (git-ignored)
├── setup.sh                 # Interactive project setup script
├── deploy.sh                # Automated deployment script
├── Dockerfile               # Container build configuration
├── docker-compose.yml       # Local development services
├── cloudbuild.yaml          # GCP Cloud Build configuration
├── .dockerignore            # Files to exclude from Docker build
├── .gcloudignore            # Files to exclude from Cloud Build
├── docs/                    # Documentation
└── tests/                   # Test files
```

## 🔧 Configuration Guide

### Docker Configuration

Edit `project.config.json` to customize:

```json
{
  "docker": {
    "imageName": "my-app-api",
    "containerName": "my-app-api",
    "port": 8080,
    "appDirectory": "/app",
    "tempDirectory": "/tmp/myapp"
  }
}
```

### Cloud Run Settings

Configure deployment settings:

```json
{
  "gcp": {
    "cloudRun": {
      "memory": "2Gi",
      "cpu": "2",
      "timeout": "600",
      "maxInstances": "10",
      "concurrency": "80"
    }
  }
}
```

### Environment-Specific Variables

Define different configurations per environment:

```json
{
  "environment": {
    "production": {
      "LOG_LEVEL": "info",
      "API_BASE_URL": "https://api.example.com"
    },
    "development": {
      "LOG_LEVEL": "debug",
      "API_BASE_URL": "http://localhost:8080"
    }
  }
}
```

## 🛠️ Customization

### For Different Technology Stacks

#### Node.js/TypeScript
```dockerfile
# In Dockerfile, update builder stage:
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage:
FROM node:20-alpine
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules /app/node_modules
CMD ["node", "dist/index.js"]
```

#### Python
```dockerfile
# Builder stage:
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Runtime:
FROM python:3.11-slim
COPY --from=builder /app /app
CMD ["python", "main.py"]
```

#### Go
```dockerfile
# Builder:
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN go build -o server

# Runtime:
FROM alpine:latest
COPY --from=builder /app/server /app/server
CMD ["/app/server"]
```

### Adding Services

Edit `docker-compose.yml` to add databases, caches, etc:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
```

## 📝 Best Practices

### Security
- ✅ Use non-root user in containers
- ✅ Keep secrets in environment variables
- ✅ Use `.env` for local development (never commit it)
- ✅ Use Google Secret Manager for production secrets
- ✅ Enable Cloud Run authentication if not public

### Performance
- ✅ Use multi-stage builds to minimize image size
- ✅ Optimize layer caching in Dockerfile
- ✅ Set appropriate memory and CPU limits
- ✅ Configure auto-scaling (min/max instances)
- ✅ Enable Cloud CDN for static assets

### Monitoring
```bash
# View Cloud Run logs
gcloud run services logs read SERVICE_NAME --limit=100

# Stream logs in real-time
gcloud run services logs tail SERVICE_NAME

# Monitor metrics
gcloud run services describe SERVICE_NAME --region REGION
```

## 🐛 Troubleshooting

### Build Failures

```bash
# Check Docker daemon is running
docker ps

# Clean Docker cache
docker system prune -a

# View build logs
docker build --progress=plain -t test .
```

### Deployment Issues

```bash
# Check GCP authentication
gcloud auth list

# Verify project access
gcloud projects describe PROJECT_ID

# Check Cloud Run service status
gcloud run services list --region REGION
```

### Common Errors

**"permission denied"**: Ensure scripts are executable
```bash
chmod +x setup.sh deploy.sh
```

**"project not found"**: Set correct GCP project
```bash
gcloud config set project YOUR_PROJECT_ID
```

**"insufficient permissions"**: Enable required APIs
```bash
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

## 🔄 Updating the Template

To use this template for a new project:

1. Clone or download this repository
2. Run `./setup.sh` to initialize configuration
3. Customize `Dockerfile` for your tech stack
4. Add your application code
5. Test locally with `docker-compose up`
6. Deploy with `./deploy.sh`

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a template repository. Feel free to customize it for your organization's needs.

---

**Need Help?** Check the documentation in the `docs/` folder or review the configuration files for inline comments and examples.
