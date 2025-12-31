# Multi-stage Docker build template
# Customize this file based on your project's technology stack

# Build arguments for configuration
ARG BASE_IMAGE=debian:bookworm-slim
ARG BUILD_IMAGE=debian:bookworm
ARG APP_DIR=/app
ARG APP_USER=appuser
ARG APP_UID=1000
ARG APP_PORT=8080

# ============================================
# Stage 1: Builder - Build your application
# ============================================
FROM ${BUILD_IMAGE} AS builder

# Install build dependencies (customize based on your stack)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    pkg-config \
    libssl-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
ARG APP_DIR
WORKDIR ${APP_DIR}

# Copy source code
COPY . .

# Build your application
# IMPORTANT: Replace this with your actual build commands
# Examples:
#   For Rust: RUN cargo build --release
#   For Go: RUN go build -o app main.go
#   For Node.js: RUN npm install && npm run build
#   For Python: RUN pip install -r requirements.txt
# RUN echo "Add your build command here" && exit 1

# ============================================
# Stage 2: Runtime - Minimal runtime image
# ============================================
FROM ${BASE_IMAGE}

# Build arguments
ARG APP_DIR
ARG APP_USER
ARG APP_UID
ARG APP_PORT
ARG TEMP_DIR=/tmp/app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u ${APP_UID} ${APP_USER} && \
    mkdir -p ${APP_DIR} ${TEMP_DIR} && \
    chown -R ${APP_USER}:${APP_USER} ${APP_DIR} ${TEMP_DIR}

WORKDIR ${APP_DIR}

# Copy built artifacts from builder stage
# IMPORTANT: Customize this based on your build output
# Examples:
#   For Rust: COPY --from=builder /app/target/release/your-binary ${APP_DIR}/
#   For Go: COPY --from=builder /app/app ${APP_DIR}/
#   For Node.js: COPY --from=builder /app/dist ${APP_DIR}/dist
#   For Python: COPY --from=builder /app ${APP_DIR}
# COPY --from=builder ${APP_DIR}/your-binary ${APP_DIR}/

# Switch to non-root user
USER ${APP_USER}

# Expose application port
EXPOSE ${APP_PORT}

# Set environment variables
ENV PORT=${APP_PORT}
ENV TEMP_DIR=${TEMP_DIR}
ENV LOG_LEVEL=info

# Health check (customize endpoint based on your app)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${APP_PORT}/health || exit 1

# Run the application
# IMPORTANT: Replace with your actual startup command
# Examples:
#   For compiled binary: CMD ["./your-binary"]
#   For Node.js: CMD ["node", "dist/index.js"]
#   For Python: CMD ["python", "main.py"]
CMD ["echo", "Configure CMD to start your application"]
