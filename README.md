# ChipaPocketOptionData

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ChipaPocketOptionData** is a powerful Python library for collecting high-volume market data from PocketOption using multiple demo accounts with optional proxy support via multiprocessing. Built on top of [BinaryOptionsToolsV2](https://github.com/ChipaDevTeam/BinaryOptionsToolsV2).

## ✨ Key Features

- 🚀 **Multi-Process Architecture**: Collect data using multiple demo accounts simultaneously
- 🔄 **High Throughput**: Leverage multiprocessing to maximize data collection speed
- 🌐 **Proxy Support**: Each process can use its own proxy server for distributed data collection
- 📊 **Multiple Data Collection Methods**:
  - Real-time symbol subscriptions
  - Time-based chunked candles
  - Count-based aggregated candles
  - Historical candle data
- �️ **Fault Tolerant**: Automatic reconnection on errors
- 📝 **Comprehensive Logging**: Built-in logging system for debugging and monitoring
- 🎯 **Simple API**: Easy-to-use interface inspired by BinaryOptionsToolsV2

## 🎯 Why ChipaPocketOptionData?

This library solves the common problem of needing high-volume market data from PocketOption:

1. **Multiple Demo Accounts**: Create several demo accounts to bypass rate limits
2. **Proxy Distribution**: Use different proxies for each account to avoid IP-based restrictions
3. **Parallel Collection**: Collect data from multiple sources simultaneously
4. **No Rate Limiting Worries**: Distribute your data collection across multiple connections

## 📦 Installation

### Using pip (recommended)

```bash
pip install ChipaPocketOptionData
```

### From source

```bash
git clone https://github.com/ChipaDevTeam/ChipaPocketOptionData.git
cd ChipaPocketOptionData
pip install -e .
```

## 🚀 Quick Start

### Basic Usage (No Proxies)

```python
from ChipaPocketOptionData import subscribe_symbol_timed
from datetime import timedelta

# Your demo account SSIDs
ssids = [
    "your_demo_ssid_1",
    "your_demo_ssid_2",
    "your_demo_ssid_3",
]

# Start collecting 5-second candles
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=timedelta(seconds=5),
    ssids=ssids,
    proxy_support=False
)

# Iterate over incoming data
for candle in collector:
    if 'error' in candle:
        print(f"Error: {candle['error']}")
        continue
    
    print(f"Candle from {candle['ssid']}: "
          f"Open={candle['open']}, Close={candle['close']}")
```

### With Proxy Support

```python
from ChipaPocketOptionData import subscribe_symbol_timed, ProxyConfig

ssids = ["ssid1", "ssid2", "ssid3"]

# Configure proxy servers
proxies = [
    ProxyConfig(host="proxy1.com", port=8080, username="user1", password="pass1"),
    ProxyConfig(host="proxy2.com", port=8080, username="user2", password="pass2"),
    ProxyConfig(host="proxy3.com", port=1080, protocol="socks5"),
]

# Start collecting with proxies
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,  # Can use int for seconds
    ssids=ssids,
    proxies=proxies,
    proxy_support=True
)

for candle in collector:
    print(f"Received: {candle}")
```

## 📚 Documentation

### Main Functions

#### `subscribe_symbol(asset, ssids, proxies=None, proxy_support=False, **config_kwargs)`

Subscribe to real-time symbol updates (1-second candles).

```python
from ChipaPocketOptionData import subscribe_symbol

collector = subscribe_symbol(
    asset="EURUSD_otc",
    ssids=["ssid1", "ssid2"],
    proxy_support=False
)

for candle in collector:
    print(candle)
```

#### `subscribe_symbol_timed(asset, time_delta, ssids, proxies=None, proxy_support=False, **config_kwargs)`

Subscribe to time-chunked symbol updates.

```python
from ChipaPocketOptionData import subscribe_symbol_timed
from datetime import timedelta

collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=timedelta(seconds=5),  # or just: time_delta=5
    ssids=["ssid1", "ssid2"],
    proxy_support=False
)

for candle in collector:
    print(candle)  # 5-second aggregated candles
```

#### `subscribe_symbol_chunked(asset, chunk_size, ssids, proxies=None, proxy_support=False, **config_kwargs)`

Subscribe to chunk-aggregated symbol updates.

```python
from ChipaPocketOptionData import subscribe_symbol_chunked

collector = subscribe_symbol_chunked(
    asset="EURUSD_otc",
    chunk_size=15,  # Aggregate every 15 candles
    ssids=["ssid1", "ssid2"],
    proxy_support=False
)

for candle in collector:
    print(candle)  # Aggregated from 15 candles
```

#### `get_candles(asset, period, time, ssids, proxies=None, proxy_support=False, **config_kwargs)`

Get historical candles (non-streaming).

```python
from ChipaPocketOptionData import get_candles

candles = get_candles(
    asset="EURUSD_otc",
    period=60,  # 1-minute candles
    time=3600,  # Last hour
    ssids=["ssid1", "ssid2"]
)

print(f"Collected {len(candles)} candles")
```

### Configuration

#### DataCollectorConfig

```python
from ChipaPocketOptionData import DataCollectorConfig, ProxyConfig

config = DataCollectorConfig(
    ssids=["ssid1", "ssid2"],
    proxies=[ProxyConfig(host="proxy.com", port=8080)],
    proxy_support=True,
    max_workers=2,  # Defaults to len(ssids)
    reconnect_on_error=True,
    error_retry_delay=5,  # seconds
    log_level="INFO",
    log_path="./logs"
)
```

#### ProxyConfig

```python
from ChipaPocketOptionData import ProxyConfig

# HTTP proxy with auth
proxy = ProxyConfig(
    host="proxy.example.com",
    port=8080,
    username="user",
    password="pass",
    protocol="http"
)

# SOCKS5 proxy without auth
proxy = ProxyConfig(
    host="proxy.example.com",
    port=1080,
    protocol="socks5"
)
```

## 📖 Examples

Check out the [examples/](examples/) directory for more detailed examples:

- **[basic_usage.py](examples/basic_usage.py)**: Simple data collection without proxies
- **[with_proxy_support.py](examples/with_proxy_support.py)**: Using multiple proxies
- **[save_to_database.py](examples/save_to_database.py)**: Storing data in SQLite
- **[multiple_assets.py](examples/multiple_assets.py)**: Collecting from multiple assets simultaneously

## 🔧 Advanced Usage

### Context Manager

```python
from ChipaPocketOptionData import subscribe_symbol_timed

ssids = ["ssid1", "ssid2"]

with subscribe_symbol_timed("EURUSD_otc", 5, ssids=ssids) as collector:
    for i, candle in enumerate(collector):
        print(candle)
        if i >= 100:
            break
# Automatically cleaned up
```

### Error Handling

```python
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=["ssid1", "ssid2"],
    reconnect_on_error=True,
    error_retry_delay=10
)

for candle in collector:
    if 'error' in candle:
        print(f"Error from {candle['ssid']}: {candle['error']}")
        # Error is logged, connection will be retried
        continue
    
    # Process valid candle
    process_candle(candle)
```

### Logging

```python
collector = subscribe_symbol_timed(
    asset="EURUSD_otc",
    time_delta=5,
    ssids=["ssid1", "ssid2"],
    log_level="DEBUG",  # DEBUG, INFO, WARN, ERROR
    log_path="./logs"   # Log directory
)
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Main Process                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │       MultiProcessDataCollector                   │ │
│  │  - Manages worker processes                       │ │
│  │  - Aggregates data from queue                     │ │
│  │  - Handles graceful shutdown                      │ │
│  └───────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
      ▼            ▼            ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Worker 1 │ │ Worker 2 │ │ Worker N │
│ SSID 1   │ │ SSID 2   │ │ SSID N   │
│ Proxy 1  │ │ Proxy 2  │ │ Proxy N  │
│          │ │          │ │          │
│ BO2 API  │ │ BO2 API  │ │ BO2 API  │
└─────┬────┘ └─────┬────┘ └─────┬────┘
      │            │            │
      └────────────┼────────────┘
                   │
                   ▼
           ┌───────────────┐
           │ Shared Queue  │
           │ (Thread-safe) │
           └───────────────┘
```

## 📋 Requirements

- Python 3.8+
- BinaryOptionsToolsV2 >= 1.0.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of [BinaryOptionsToolsV2](https://github.com/ChipaDevTeam/BinaryOptionsToolsV2)
- Inspired by the need for high-volume data collection from PocketOption

## 📧 Support

If you have any questions or issues, please:

1. Check the [examples/](examples/) directory
2. Open an issue on [GitHub](https://github.com/ChipaDevTeam/ChipaPocketOptionData/issues)

## ⚠️ Disclaimer

This library is for educational and research purposes only. Use at your own risk. Make sure to comply with PocketOption's Terms of Service.

---

Made with ❤️ by the ChipaDev Team

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
