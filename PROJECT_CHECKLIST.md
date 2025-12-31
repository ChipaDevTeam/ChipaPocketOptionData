# 📋 New Project Checklist

Use this checklist when starting a new project with this template.

## 🎬 Initial Setup

### Configuration
- [ ] Run `./setup.sh` and answer all prompts
- [ ] Review generated `project.config.json`
- [ ] Copy `.env.example` to `.env` (done by setup.sh)
- [ ] Update `.env` with your actual values
- [ ] Run `./validate.sh` to check configuration

### Repository
- [ ] Initialize git repository: `git init`
- [ ] Create `.gitignore` (already included)
- [ ] Review and update `LICENSE` file
- [ ] Create GitHub/GitLab repository
- [ ] Push initial commit

### Documentation
- [ ] Update `README.md` with project-specific info
- [ ] Remove `TEMPLATE_USAGE.md` or adapt for team
- [ ] Keep `DEPLOYMENT_SUMMARY.md` as reference
- [ ] Update `CHANGELOG.md` with v1.0.0 entry

## 🛠️ Development Setup

### Code
- [ ] Choose your tech stack (Node.js/Python/Go/Rust)
- [ ] Update `Dockerfile` with your build commands
- [ ] Remove placeholder commands from Dockerfile
- [ ] Create source directory: `mkdir -p src`
- [ ] Add your application code
- [ ] Update health check endpoint if not `/health`

### Dependencies
- [ ] Add package manager files (package.json, requirements.txt, go.mod, Cargo.toml)
- [ ] Install dependencies locally
- [ ] Test build locally: `docker build -t test .`

### Docker Compose
- [ ] Review `docker-compose.yml` services
- [ ] Add database if needed (PostgreSQL/MySQL/MongoDB)
- [ ] Add cache if needed (Redis/Memcached)
- [ ] Update volume mounts for development
- [ ] Configure environment variables

## 🧪 Testing

### Local Testing
- [ ] Build containers: `docker-compose build`
- [ ] Start services: `docker-compose up`
- [ ] Test health endpoint: `curl http://localhost:8080/health`
- [ ] Test main functionality
- [ ] Check logs: `docker-compose logs`
- [ ] Stop services: `docker-compose down`

### Code Quality
- [ ] Set up testing framework
- [ ] Write unit tests (see `tests/README-tests.md`)
- [ ] Set up linting
- [ ] Configure code formatting
- [ ] Add pre-commit hooks

## ☁️ Cloud Setup

### GCP Prerequisites
- [ ] Create GCP project or select existing
- [ ] Enable billing on the project
- [ ] Install `gcloud` CLI
- [ ] Authenticate: `gcloud auth login`
- [ ] Set project: `gcloud config set project PROJECT_ID`
- [ ] Update `project.config.json` with GCP project ID
- [ ] Update `.env` with `GCP_PROJECT_ID`

### Enable APIs
- [ ] Cloud Run API
- [ ] Cloud Build API
- [ ] Container Registry API
- [ ] Artifact Registry API (optional)

### IAM & Permissions
- [ ] Create service account for deployments (if using CI/CD)
- [ ] Grant Cloud Run Admin role
- [ ] Grant Storage Admin role
- [ ] Grant Cloud Build Service Account role
- [ ] Download service account key (for CI/CD)

## 🚀 First Deployment

### Pre-deployment
- [ ] Review `project.config.json` settings
- [ ] Run `./validate.sh`
- [ ] Test Docker build locally
- [ ] Ensure no secrets in code/configs
- [ ] Review Cloud Run settings (memory, CPU, timeout)

### Deploy
- [ ] Run `./deploy.sh`
- [ ] Note the service URL
- [ ] Test health endpoint on Cloud Run
- [ ] Test main functionality on Cloud Run
- [ ] Check Cloud Run logs: `gcloud run services logs read SERVICE_NAME`

### Post-deployment
- [ ] Set up custom domain (optional)
- [ ] Configure Cloud CDN (optional)
- [ ] Set up monitoring and alerts
- [ ] Configure backup strategy (if using database)
- [ ] Document deployment procedures for team

## 🔄 CI/CD Setup (Optional)

### GitHub Actions
- [ ] Copy `.github/workflows/deploy.yml.example` to `.github/workflows/deploy.yml`
- [ ] Update workflow with your settings
- [ ] Add GitHub secrets:
  - `GCP_PROJECT_ID`
  - `GCP_SA_KEY`
  - `SERVICE_NAME`
- [ ] Test workflow by pushing to main branch

### Other CI/CD Platforms
- [ ] GitLab CI: Create `.gitlab-ci.yml`
- [ ] CircleCI: Create `.circleci/config.yml`
- [ ] Jenkins: Set up pipeline
- [ ] Configure triggers and notifications

## 📊 Monitoring & Operations

### Monitoring
- [ ] Set up Cloud Monitoring dashboards
- [ ] Configure uptime checks
- [ ] Set up error reporting
- [ ] Configure log-based metrics
- [ ] Set up alerting policies

### Logging
- [ ] Review log levels (info/debug/error)
- [ ] Set up log aggregation
- [ ] Configure log retention
- [ ] Add structured logging

### Security
- [ ] Review security settings
- [ ] Enable Cloud Armor (if needed)
- [ ] Configure IAM roles properly
- [ ] Set up Secret Manager for secrets
- [ ] Enable VPC Service Controls (if applicable)
- [ ] Review security scanning results

## 📝 Documentation

### Team Documentation
- [ ] Document architecture in `docs/`
- [ ] Create API documentation
- [ ] Document environment setup
- [ ] Add troubleshooting guide
- [ ] Document deployment procedures

### Code Documentation
- [ ] Add inline comments
- [ ] Document complex functions
- [ ] Create README for each major component
- [ ] Update CHANGELOG.md

## 🎯 Production Readiness

### Performance
- [ ] Load test your application
- [ ] Optimize Docker image size
- [ ] Configure auto-scaling properly
- [ ] Set appropriate resource limits
- [ ] Enable caching where appropriate

### Reliability
- [ ] Implement health checks
- [ ] Add readiness/liveness probes
- [ ] Configure graceful shutdown
- [ ] Test failure scenarios
- [ ] Document disaster recovery plan

### Costs
- [ ] Review resource allocation
- [ ] Set up cost monitoring
- [ ] Configure cost alerts
- [ ] Optimize for cost (right-size instances)

## ✅ Final Checks

Before announcing to team:
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Deployment working
- [ ] Monitoring set up
- [ ] Team has access
- [ ] Runbooks created
- [ ] Backup strategy tested

## 🎉 Go Live

- [ ] Announce to stakeholders
- [ ] Monitor closely for first 24 hours
- [ ] Be ready for quick rollback if needed
- [ ] Gather feedback
- [ ] Plan next iterations

---

## 📚 References

- Main docs: `README.md`
- Template guide: `TEMPLATE_USAGE.md`
- Testing guide: `tests/README-tests.md`
- Cloud Run docs: https://cloud.google.com/run/docs

## 💡 Tips

1. **Start small**: Get basic deployment working first
2. **Iterate**: Add features gradually
3. **Document**: Write docs as you go
4. **Monitor**: Watch logs and metrics closely
5. **Automate**: Use CI/CD from the start

---

**Good luck with your project!** 🚀

*Save this checklist and mark items as you complete them!*
