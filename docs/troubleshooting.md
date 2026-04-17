# Pet Shop Troubleshooting Guide

This guide helps you diagnose and resolve common issues with the Pet Shop application.

## Common Issues

### Application Won't Start

**Symptoms**: Application crashes on startup or won't start

**Possible Causes & Solutions**:

1. **Port Already in Use**
   ```bash
   # Find process using port 3000
   lsof -i :3000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Missing Environment Variables**
   - Check `.env` file exists
   - Verify all required variables are set
   - Run: `npm run check-env`

3. **Database Connection Failed**
   ```bash
   # Test database connection
   psql -U postgres -h localhost -d petshop
   
   # Check if database exists
   psql -U postgres -l
   ```

### Database Issues

#### Connection Errors

**Error**: `ECONNREFUSED` or `Connection timeout`

**Solutions**:
1. Verify database is running:
   ```bash
   # PostgreSQL
   systemctl status postgresql
   
   # Or check Docker container
   docker ps | grep postgres
   ```

2. Check connection string in `.env`
3. Verify firewall rules allow database access
4. Test network connectivity

#### Migration Failures

**Error**: Migration fails or hangs

**Solutions**:
```bash
# Roll back last migration
npm run migrate:rollback

# Check migration status
npm run migrate:status

# Manually fix and re-run
npm run migrate
```

### Redis Connection Issues

**Symptoms**: Caching not working, session errors

**Solutions**:
1. Check Redis is running:
   ```bash
   redis-cli ping
   # Should return: PONG
   ```

2. Verify Redis URL in configuration
3. Check Redis logs:
   ```bash
   docker logs petshop_redis
   ```

### Performance Issues

#### Slow Page Load Times

**Diagnostic Steps**:
1. Check server resources:
   ```bash
   top
   htop
   ```

2. Monitor database queries:
   ```sql
   -- Show slow queries
   SELECT * FROM pg_stat_statements 
   ORDER BY mean_exec_time DESC LIMIT 10;
   ```

3. Check Redis cache hit rate:
   ```bash
   redis-cli INFO stats
   ```

**Solutions**:
- Enable query caching
- Optimize database indexes
- Implement CDN for static assets
- Scale horizontally

#### High Memory Usage

**Solutions**:
1. Identify memory leaks:
   ```bash
   node --inspect app.js
   ```

2. Limit Node.js memory:
   ```bash
   node --max-old-space-size=4096 app.js
   ```

3. Review and optimize code
4. Increase server resources

### API Errors

#### 401 Unauthorized

**Causes**:
- Expired JWT token
- Invalid credentials
- Missing Authorization header

**Solutions**:
1. Refresh authentication token
2. Verify API key is correct
3. Check token expiration time

#### 429 Too Many Requests

**Cause**: Rate limit exceeded

**Solutions**:
- Wait before retrying
- Implement exponential backoff
- Contact support for limit increase

#### 500 Internal Server Error

**Debugging**:
1. Check application logs:
   ```bash
   tail -f logs/error.log
   ```

2. Enable debug mode:
   ```bash
   DEBUG=* npm start
   ```

3. Review stack trace
4. Check database connectivity

### Docker Issues

#### Container Won't Start

**Solutions**:
```bash
# View container logs
docker logs petshop_web

# Inspect container
docker inspect petshop_web

# Restart container
docker-compose restart web

# Rebuild container
docker-compose build --no-cache web
docker-compose up -d
```

#### Volume Permission Issues

**Error**: Permission denied accessing volumes

**Solution**:
```bash
# Fix permissions
sudo chown -R $(whoami):$(whoami) ./volumes

# Or run with correct user
docker-compose run --user $(id -u):$(id -g) web
```

### Frontend Issues

#### JavaScript Errors in Browser

**Debugging**:
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Review Network tab for failed requests
4. Clear browser cache and cookies

#### Styles Not Loading

**Solutions**:
1. Check CSS file paths
2. Verify build process completed
3. Clear browser cache
4. Check CDN availability

### Authentication Issues

#### Can't Log In

**Solutions**:
1. Verify credentials are correct
2. Check if account is activated
3. Reset password if needed
4. Clear browser cookies
5. Try incognito mode

#### Session Expires Too Quickly

**Solution**:
Adjust session timeout in configuration:
```javascript
// config.js
sessionTimeout: 3600 // 1 hour in seconds
```

### Deployment Issues

#### Kubernetes Pod Crashes

**Debugging**:
```bash
# Check pod status
kubectl get pods -n production

# View pod logs
kubectl logs -f <pod-name> -n production

# Describe pod for events
kubectl describe pod <pod-name> -n production

# Check resource limits
kubectl top pods -n production
```

#### Failed Health Checks

**Solutions**:
1. Increase health check timeout
2. Fix application startup issues
3. Verify health endpoint is accessible
4. Check resource constraints

### Email Notifications Not Sending

**Possible Causes**:
1. SMTP settings incorrect
2. Firewall blocking port 587/465
3. Invalid sender email
4. Email service down

**Solutions**:
```bash
# Test SMTP connection
telnet smtp.gmail.com 587

# Check email queue
npm run email:check-queue

# Retry failed emails
npm run email:retry-failed
```

### File Upload Issues

#### Upload Fails

**Solutions**:
1. Check file size limits
2. Verify storage permissions
3. Check available disk space:
   ```bash
   df -h
   ```
4. Review upload directory permissions

## Debug Mode

Enable detailed logging:

```bash
# Set environment variable
export DEBUG=petshop:*

# Or in .env file
DEBUG=petshop:*
LOG_LEVEL=debug
```

## Getting Help

### Before Contacting Support

1. Check error logs
2. Review this troubleshooting guide
3. Search existing GitHub issues
4. Try clearing cache/cookies

### Contact Support

- **Email**: support@petshop.com
- **Live Chat**: Available 9 AM - 9 PM EST
- **Phone**: (555) 123-4567
- **GitHub Issues**: https://github.com/petshop/issues

### Emergency Contact

For production-critical issues:
- **Hotline**: (555) 999-9999 (24/7)
- **Slack**: #petshop-emergency

## Useful Commands

### Check Application Status
```bash
npm run status
```

### Run Diagnostics
```bash
npm run diagnostics
```

### Clear All Caches
```bash
npm run cache:clear
```

### Reset Development Environment
```bash
npm run reset:dev
```

### View All Logs
```bash
npm run logs:all
```

## Additional Resources

- [GitHub Wiki](https://github.com/petshop/wiki)
- [Stack Overflow Tag](https://stackoverflow.com/questions/tagged/petshop)
- [Community Forum](https://community.petshop.com)
- [Video Tutorials](https://youtube.com/petshop)
