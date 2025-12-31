#!/bin/bash
# Template Initialization Script
# This script helps you quickly set up a new project from this template

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Project Template Initialization Script             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  'jq' is not installed. Installing it is recommended for easier setup.${NC}"
    echo "   Install with: brew install jq (macOS) or apt-get install jq (Linux)"
    echo ""
fi

# Function to prompt for input with default value
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local result
    
    if [ -n "$default" ]; then
        read -p "$(echo -e ${BLUE}$prompt ${NC}[${default}]: )" result
        echo "${result:-$default}"
    else
        read -p "$(echo -e ${BLUE}$prompt ${NC}: )" result
        while [ -z "$result" ]; do
            echo -e "${RED}This field is required${NC}"
            read -p "$(echo -e ${BLUE}$prompt ${NC}: )" result
        done
        echo "$result"
    fi
}

# Gather project information
echo -e "${YELLOW}Let's configure your new project!${NC}"
echo ""

PROJECT_NAME=$(prompt_with_default "Project name (lowercase, no spaces)" "my-project")
PROJECT_DISPLAY_NAME=$(prompt_with_default "Project display name" "My Project")
PROJECT_DESCRIPTION=$(prompt_with_default "Project description" "A new project")
SERVICE_PORT=$(prompt_with_default "Service port" "8080")
DOCKER_IMAGE_NAME=$(prompt_with_default "Docker image name" "${PROJECT_NAME}-api")
CONTAINER_NAME=$(prompt_with_default "Container name" "${PROJECT_NAME}-api")

echo ""
echo -e "${YELLOW}GCP Configuration (optional - press Enter to skip)${NC}"
GCP_PROJECT_ID=$(prompt_with_default "GCP Project ID" "")
GCP_REGION=$(prompt_with_default "GCP Region" "us-central1")
GCP_SERVICE_NAME=$(prompt_with_default "Cloud Run service name" "${PROJECT_NAME}-api")

echo ""
echo -e "${YELLOW}Build Configuration${NC}"
APP_DIR=$(prompt_with_default "Application directory in container" "/app")
TEMP_DIR=$(prompt_with_default "Temporary directory" "/tmp/${PROJECT_NAME}")
BINARY_NAME=$(prompt_with_default "Binary/executable name" "api-server")
HEALTH_ENDPOINT=$(prompt_with_default "Health check endpoint" "/health")

# Summary
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Configuration Summary:${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo "Project Name:        $PROJECT_NAME"
echo "Display Name:        $PROJECT_DISPLAY_NAME"
echo "Description:         $PROJECT_DESCRIPTION"
echo "Port:                $SERVICE_PORT"
echo "Docker Image:        $DOCKER_IMAGE_NAME"
echo "Container Name:      $CONTAINER_NAME"
if [ -n "$GCP_PROJECT_ID" ]; then
    echo "GCP Project ID:      $GCP_PROJECT_ID"
    echo "GCP Region:          $GCP_REGION"
    echo "Cloud Run Service:   $GCP_SERVICE_NAME"
fi
echo "Binary Name:         $BINARY_NAME"
echo "Health Endpoint:     $HEALTH_ENDPOINT"
echo ""

read -p "$(echo -e ${YELLOW}Proceed with this configuration? ${NC}[y/N]: )" confirm
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo -e "${RED}Setup cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}Updating configuration files...${NC}"

# Update project.config.json
if command -v jq &> /dev/null; then
    jq --arg name "$PROJECT_NAME" \
       --arg displayName "$PROJECT_DISPLAY_NAME" \
       --arg description "$PROJECT_DESCRIPTION" \
       --arg imageName "$DOCKER_IMAGE_NAME" \
       --arg containerName "$CONTAINER_NAME" \
       --argjson port "$SERVICE_PORT" \
       --arg appDir "$APP_DIR" \
       --arg tempDir "$TEMP_DIR" \
       --arg binaryName "$BINARY_NAME" \
       --arg healthCheck "$HEALTH_ENDPOINT" \
       --arg gcpProjectId "$GCP_PROJECT_ID" \
       --arg gcpRegion "$GCP_REGION" \
       --arg gcpServiceName "$GCP_SERVICE_NAME" \
       '.project.name = $name |
        .project.displayName = $displayName |
        .project.description = $description |
        .docker.imageName = $imageName |
        .docker.containerName = $containerName |
        .docker.port = $port |
        .docker.appDirectory = $appDir |
        .docker.tempDirectory = $tempDir |
        .build.binaryName = $binaryName |
        .build.healthCheckEndpoint = $healthCheck |
        .gcp.projectId = $gcpProjectId |
        .gcp.region = $gcpRegion |
        .gcp.serviceName = $gcpServiceName' \
       project.config.json > project.config.json.tmp && mv project.config.json.tmp project.config.json
    
    echo -e "${GREEN}✓ Updated project.config.json${NC}"
else
    echo -e "${YELLOW}⚠️  Skipping automatic config update (jq not installed)${NC}"
    echo "   Please manually edit project.config.json"
fi

# Create .env file from .env.example
if [ -f ".env.example" ]; then
    cp .env.example .env
    
    # Replace placeholders in .env
    sed -i.bak "s|PROJECT_NAME=.*|PROJECT_NAME=${PROJECT_NAME}|g" .env
    sed -i.bak "s|PORT=.*|PORT=${SERVICE_PORT}|g" .env
    sed -i.bak "s|TEMP_DIR=.*|TEMP_DIR=${TEMP_DIR}|g" .env
    
    if [ -n "$GCP_PROJECT_ID" ]; then
        sed -i.bak "s|GCP_PROJECT_ID=.*|GCP_PROJECT_ID=${GCP_PROJECT_ID}|g" .env
    fi
    
    rm -f .env.bak
    echo -e "${GREEN}✓ Created .env file${NC}"
fi

# Update README.md title
if [ -f "README.md" ]; then
    sed -i.bak "1s/.*/# ${PROJECT_DISPLAY_NAME}/" README.md
    sed -i.bak "2s/.*/${PROJECT_DESCRIPTION}/" README.md
    rm -f README.md.bak
    echo -e "${GREEN}✓ Updated README.md${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Initialization Complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Review and edit configuration files:"
echo "   - project.config.json (project settings)"
echo "   - .env (environment variables)"
echo "   - Dockerfile (container build)"
echo ""
echo "2. Add your application source code to the project"
echo ""
echo "3. Test locally with Docker:"
echo "   docker-compose up --build"
echo ""
echo "4. Deploy to production:"
echo "   ./deploy.sh"
echo ""
echo -e "${YELLOW}📚 See README.md for detailed documentation${NC}"
echo ""
