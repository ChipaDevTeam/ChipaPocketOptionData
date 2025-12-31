#!/bin/bash
set -e

# Generic Cloud Run Deployment Script
# Reads configuration from project.config.json and .env

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load configuration
CONFIG_FILE="project.config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}❌ Configuration file not found: ${CONFIG_FILE}${NC}"
    echo "Run ./setup.sh first to initialize your project"
    exit 1
fi

# Check if jq is available for parsing JSON
if command -v jq &> /dev/null; then
    # Extract configuration from JSON
    PROJECT_NAME=$(jq -r '.project.name' "$CONFIG_FILE")
    SERVICE_NAME=$(jq -r '.gcp.serviceName' "$CONFIG_FILE")
    GCP_PROJECT_ID=$(jq -r '.gcp.projectId' "$CONFIG_FILE")
    REGION=$(jq -r '.gcp.region' "$CONFIG_FILE")
    MEMORY=$(jq -r '.gcp.cloudRun.memory' "$CONFIG_FILE")
    CPU=$(jq -r '.gcp.cloudRun.cpu' "$CONFIG_FILE")
    TIMEOUT=$(jq -r '.gcp.cloudRun.timeout' "$CONFIG_FILE")
    MAX_INSTANCES=$(jq -r '.gcp.cloudRun.maxInstances' "$CONFIG_FILE")
    CONCURRENCY=$(jq -r '.gcp.cloudRun.concurrency' "$CONFIG_FILE")
    ALLOW_UNAUTH=$(jq -r '.gcp.cloudRun.allowUnauthenticated' "$CONFIG_FILE")
else
    echo -e "${YELLOW}⚠️  'jq' not found. Using default/environment variables${NC}"
    PROJECT_NAME="${PROJECT_NAME:-my-project}"
    SERVICE_NAME="${SERVICE_NAME:-my-project-api}"
    GCP_PROJECT_ID="${GCP_PROJECT_ID:-}"
    REGION="${REGION:-us-central1}"
    MEMORY="${MEMORY:-2Gi}"
    CPU="${CPU:-2}"
    TIMEOUT="${TIMEOUT:-600}"
    MAX_INSTANCES="${MAX_INSTANCES:-10}"
    CONCURRENCY="${CONCURRENCY:-80}"
    ALLOW_UNAUTH="${ALLOW_UNAUTH:-true}"
fi

# Override with environment variables if set
PROJECT_ID="${GCP_PROJECT_ID:-${PROJECT_ID}}"
REGION="${REGION:-us-central1}"
USE_LOCAL_BUILD="${USE_LOCAL_BUILD:-true}"  # Default to local builds

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           Cloud Run Deployment Script                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}Project: ${PROJECT_NAME}${NC}"
echo -e "${YELLOW}Service: ${SERVICE_NAME}${NC}"
echo "================================================"

# Check if Docker is installed (required for local builds)
if [ "$USE_LOCAL_BUILD" = "true" ]; then
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed (required for local builds)${NC}"
        echo "Install it from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker found - using local builds${NC}"
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed${NC}"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if PROJECT_ID is set
if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "null" ]; then
    echo -e "${YELLOW}No PROJECT_ID set. Available projects:${NC}"
    gcloud projects list
    echo ""
    read -p "Enter your GCP Project ID: " PROJECT_ID
    
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ PROJECT_ID is required${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✓ Using Project: ${PROJECT_ID}${NC}"
echo -e "${GREEN}✓ Using Region: ${REGION}${NC}"
echo ""

# Set the project
echo -e "${YELLOW}Setting GCP project...${NC}"
gcloud config set project "$PROJECT_ID"

# Enable required APIs
echo -e "${YELLOW}Enabling required APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    artifactregistry.googleapis.com

# Build and deploy
echo ""
BUILD_TAG=$(date +%Y%m%d-%H%M%S)
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:${BUILD_TAG}"
LATEST_IMAGE="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

if [ "$USE_LOCAL_BUILD" = "true" ]; then
    echo -e "${YELLOW}🔨 Building Docker image locally...${NC}"
    echo "This may take a few minutes..."
    echo ""
    
    # Build locally with Docker
    docker build --platform linux/amd64 -t "$IMAGE_NAME" -t "$LATEST_IMAGE" .
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Docker build failed${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${YELLOW}📤 Pushing image to Google Container Registry...${NC}"
    
    # Configure Docker to use gcloud as credential helper
    gcloud auth configure-docker --quiet
    
    # Push the image
    docker push "$IMAGE_NAME"
    docker push "$LATEST_IMAGE"
    
    echo -e "${GREEN}✓ Image pushed successfully${NC}"
else
    echo -e "${YELLOW}🔨 Building with Cloud Build...${NC}"
    echo "This will take several minutes..."
    echo ""
    
    gcloud builds submit \
        --config=cloudbuild.yaml \
        --region="$REGION" \
        --substitutions="_SERVICE_NAME=${SERVICE_NAME},COMMIT_SHA=${BUILD_TAG},_REGION=${REGION},_MEMORY=${MEMORY},_CPU=${CPU},_TIMEOUT=${TIMEOUT},_MAX_INSTANCES=${MAX_INSTANCES},_CONCURRENCY=${CONCURRENCY}"
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Cloud Build failed${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Build completed successfully${NC}"
fi

# Deploy to Cloud Run (if using local build, or as additional step)
if [ "$USE_LOCAL_BUILD" = "true" ]; then
    echo ""
    echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"

    ALLOW_UNAUTH_FLAG=""
    if [ "$ALLOW_UNAUTH" = "true" ]; then
        ALLOW_UNAUTH_FLAG="--allow-unauthenticated"
    else
        ALLOW_UNAUTH_FLAG="--no-allow-unauthenticated"
    fi

    gcloud run deploy "$SERVICE_NAME" \
        --image="$IMAGE_NAME" \
        --region="$REGION" \
        --platform=managed \
        $ALLOW_UNAUTH_FLAG \
        --memory="$MEMORY" \
        --cpu="$CPU" \
        --timeout="$TIMEOUT" \
        --max-instances="$MAX_INSTANCES" \
        --concurrency="$CONCURRENCY"
        # Add environment variables from .env if needed
        # --set-env-vars="$(cat .env | grep -v '^#' | xargs)"
fi

# Get the service URL
echo ""
echo -e "${GREEN}✅ Deployment successful!${NC}"
echo ""
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format="value(status.url)")

echo "================================================"
echo -e "${GREEN}🎉 ${PROJECT_NAME} is live!${NC}"
echo "================================================"
echo ""
echo "Service URL: ${SERVICE_URL}"
echo ""
echo "Test the health endpoint:"
echo "  curl ${SERVICE_URL}/health"
echo ""
echo "View logs:"
echo "  gcloud run services logs read ${SERVICE_NAME} --region=${REGION} --limit=50"
echo ""
echo "Monitor service:"
echo "  gcloud run services describe ${SERVICE_NAME} --region=${REGION}"
echo ""
