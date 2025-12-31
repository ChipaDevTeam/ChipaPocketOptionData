#!/bin/bash
# Quick validation script to check if the template is properly configured

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔍 Template Configuration Validator"
echo "===================================="
echo ""

ERRORS=0
WARNINGS=0

# Check for required files
echo "Checking required files..."

REQUIRED_FILES=(
    "project.config.json"
    ".env"
    "Dockerfile"
    "docker-compose.yml"
    "deploy.sh"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} $file exists"
    else
        echo -e "${RED}✗${NC} $file missing"
        ((ERRORS++))
    fi
done

echo ""

# Check if scripts are executable
echo "Checking script permissions..."

SCRIPTS=("setup.sh" "deploy.sh")

for script in "${SCRIPTS[@]}"; do
    if [ -x "$script" ]; then
        echo -e "${GREEN}✓${NC} $script is executable"
    else
        echo -e "${YELLOW}⚠${NC}  $script is not executable (run: chmod +x $script)"
        ((WARNINGS++))
    fi
done

echo ""

# Validate project.config.json
echo "Validating project.config.json..."

if [ -f "project.config.json" ]; then
    # Check if jq is available
    if command -v jq &> /dev/null; then
        # Validate JSON syntax
        if jq empty project.config.json 2>/dev/null; then
            echo -e "${GREEN}✓${NC} JSON syntax is valid"
            
            # Check for default/placeholder values
            PROJECT_NAME=$(jq -r '.project.name' project.config.json)
            if [ "$PROJECT_NAME" = "my-project" ]; then
                echo -e "${YELLOW}⚠${NC}  Project name is still default 'my-project'"
                ((WARNINGS++))
            fi
            
            GCP_PROJECT=$(jq -r '.gcp.projectId' project.config.json)
            if [ -z "$GCP_PROJECT" ] || [ "$GCP_PROJECT" = "null" ] || [ "$GCP_PROJECT" = "" ]; then
                echo -e "${YELLOW}⚠${NC}  GCP Project ID not set (required for deployment)"
                ((WARNINGS++))
            fi
        else
            echo -e "${RED}✗${NC} Invalid JSON syntax"
            ((ERRORS++))
        fi
    else
        echo -e "${YELLOW}⚠${NC}  jq not installed, skipping JSON validation"
        ((WARNINGS++))
    fi
fi

echo ""

# Check .env file
echo "Checking .env configuration..."

if [ -f ".env" ]; then
    # Check for placeholder values
    if grep -q "example.com" .env 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC}  .env contains example URLs (update with real values)"
        ((WARNINGS++))
    fi
    
    if grep -q "GCP_PROJECT_ID=$" .env 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC}  GCP_PROJECT_ID is empty in .env"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC}  .env file not found (copy from .env.example)"
    ((WARNINGS++))
fi

echo ""

# Check Dockerfile
echo "Checking Dockerfile..."

if [ -f "Dockerfile" ]; then
    if grep -q "Add your build command here" Dockerfile; then
        echo -e "${YELLOW}⚠${NC}  Dockerfile contains placeholder build commands"
        ((WARNINGS++))
    fi
    
    if grep -q "Configure CMD to start your application" Dockerfile; then
        echo -e "${YELLOW}⚠${NC}  Dockerfile CMD needs to be configured"
        ((WARNINGS++))
    fi
fi

echo ""

# Check if Docker is running
echo "Checking Docker..."

if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker is installed"
    
    if docker ps &> /dev/null; then
        echo -e "${GREEN}✓${NC} Docker daemon is running"
    else
        echo -e "${YELLOW}⚠${NC}  Docker daemon is not running"
        ((WARNINGS++))
    fi
else
    echo -e "${YELLOW}⚠${NC}  Docker is not installed (required for local development)"
    ((WARNINGS++))
fi

echo ""

# Check gcloud CLI
echo "Checking GCP tools..."

if command -v gcloud &> /dev/null; then
    echo -e "${GREEN}✓${NC} gcloud CLI is installed"
    
    # Check if authenticated
    if gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
        ACTIVE_ACCOUNT=$(gcloud auth list --filter=status:ACTIVE --format="value(account)" 2>/dev/null | head -n 1)
        if [ -n "$ACTIVE_ACCOUNT" ]; then
            echo -e "${GREEN}✓${NC} Authenticated as: $ACTIVE_ACCOUNT"
        else
            echo -e "${YELLOW}⚠${NC}  Not authenticated with gcloud (run: gcloud auth login)"
            ((WARNINGS++))
        fi
    fi
else
    echo -e "${YELLOW}⚠${NC}  gcloud CLI not installed (required for GCP deployment)"
    ((WARNINGS++))
fi

echo ""
echo "===================================="

# Summary
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ All checks passed!${NC}"
    echo ""
    echo "Your template is properly configured."
    echo "Next steps:"
    echo "  1. Review and update project.config.json"
    echo "  2. Customize Dockerfile for your tech stack"
    echo "  3. Add your application code"
    echo "  4. Test locally: docker-compose up"
    echo "  5. Deploy: ./deploy.sh"
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  Configuration complete with $WARNINGS warning(s)${NC}"
    echo ""
    echo "Review the warnings above before deploying."
else
    echo -e "${RED}❌ Found $ERRORS error(s) and $WARNINGS warning(s)${NC}"
    echo ""
    echo "Please fix the errors before proceeding."
    exit 1
fi

echo ""
