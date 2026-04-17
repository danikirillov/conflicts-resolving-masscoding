# Pet Shop Deployment Guide

This guide covers deploying the Pet Shop application to production environments.

## Deployment Options

1. Docker Containers
2. Kubernetes
3. Traditional Server Deployment
4. Serverless (AWS Lambda/Azure Functions)

## Prerequisites

- Production database (PostgreSQL)
- Redis instance
- SSL certificates
- Domain name configured
- CI/CD pipeline access

## Docker Deployment

### 1. Build Docker Image

```bash
docker build -t petshop-web:latest .
```

### 2. Push to Registry

```bash
docker tag petshop-web:latest your-registry.com/petshop-web:latest
docker push your-registry.com/petshop-web:latest
```

### 3. Deploy with Docker Compose

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Kubernetes Deployment

### 1. Create Namespace

```bash
kubectl create namespace production
```

### 2. Apply Secrets

```bash
kubectl create secret generic petshop-secrets \
  --from-literal=database-url=postgresql://... \
  --from-literal=db-username=admin \
  --from-literal=db-password=securepassword \
  -n production
```

### 3. Deploy Application

```bash
kubectl apply -f devops/kubernetes-deployment.yaml
```

### 4. Verify Deployment

```bash
kubectl get pods -n production
kubectl get services -n production
```

### 5. Check Logs

```bash
kubectl logs -f deployment/petshop-web -n production
```

## Environment Configuration

### Production Environment Variables

```bash
NODE_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/petshop
REDIS_URL=redis://redis-host:6379
PORT=3000
JWT_SECRET=your-secure-secret
API_KEY=your-api-key
```

### Database Configuration

1. Create production database:
```sql
CREATE DATABASE petshop_production;
```

2. Run migrations:
```bash
npm run migrate:prod
```

3. Set up read replicas for scaling

### SSL/TLS Setup

1. Obtain SSL certificates (Let's Encrypt recommended)
2. Configure nginx or load balancer
3. Force HTTPS redirects

## CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline automatically:
1. Runs tests on pull requests
2. Builds Docker images on merge
3. Deploys to staging (develop branch)
4. Deploys to production (main branch)

### Manual Deployment

If needed, trigger manual deployment:

```bash
# Deploy to staging
npm run deploy:staging

# Deploy to production
npm run deploy:production
```

## Performance Optimization

### 1. Enable Caching

Configure Redis for:
- Session management
- API response caching
- Rate limiting

### 2. CDN Setup

Configure CDN for static assets:
- Images
- CSS/JS files
- Fonts

### 3. Database Optimization

- Enable connection pooling
- Configure read replicas
- Implement query caching
- Regular index maintenance

### 4. Load Balancing

Set up load balancer for:
- Multiple app instances
- Health checks
- SSL termination
- Traffic distribution

## Monitoring Setup

### 1. Application Monitoring

Deploy monitoring stack:
```bash
kubectl apply -f devops/monitoring-stack.yaml
```

### 2. Configure Alerts

Set up alerts for:
- High error rates
- Slow response times
- Low disk space
- Database connection issues

### 3. Log Aggregation

Configure log shipping to:
- Elasticsearch
- CloudWatch
- Datadog
- Splunk

## Backup Strategy

### Database Backups

1. Automated daily backups
2. Point-in-time recovery enabled
3. Backup retention: 30 days
4. Off-site backup storage

```bash
# Manual backup
pg_dump -U postgres petshop_production > backup.sql

# Restore
psql -U postgres petshop_production < backup.sql
```

### File Storage Backups

Backup uploaded files to cloud storage:
- AWS S3
- Azure Blob Storage
- Google Cloud Storage

## Rollback Procedures

### Kubernetes Rollback

```bash
# View deployment history
kubectl rollout history deployment/petshop-web -n production

# Rollback to previous version
kubectl rollout undo deployment/petshop-web -n production

# Rollback to specific revision
kubectl rollout undo deployment/petshop-web --to-revision=3 -n production
```

### Docker Rollback

```bash
# Deploy previous image version
docker-compose down
docker-compose up -d petshop-web:v1.0.0
```

## Security Checklist

- [ ] All secrets stored in secret management system
- [ ] SSL/TLS enabled and enforced
- [ ] Database connections encrypted
- [ ] API rate limiting configured
- [ ] CORS properly configured
- [ ] Security headers set
- [ ] Regular security updates applied
- [ ] Firewall rules configured
- [ ] DDoS protection enabled

## Scaling

### Horizontal Scaling

Increase replicas:
```bash
kubectl scale deployment/petshop-web --replicas=5 -n production
```

### Auto-scaling

Configure HPA (Horizontal Pod Autoscaler):
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: petshop-web-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: petshop-web
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Health Checks

Implement health check endpoints:

- `/health` - Basic health check
- `/ready` - Readiness check
- `/metrics` - Prometheus metrics

## Post-Deployment Verification

1. **Smoke Tests**: Run critical path tests
2. **Performance Tests**: Check response times
3. **Monitor Logs**: Watch for errors
4. **Database Checks**: Verify connections
5. **User Testing**: Test core functionality

## Support & Troubleshooting

For deployment issues:
- Check deployment logs
- Review monitoring dashboards
- Contact DevOps team: devops@petshop.com
- Emergency hotline: (555) 999-9999
