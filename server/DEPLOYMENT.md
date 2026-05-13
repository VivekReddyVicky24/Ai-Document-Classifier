# Deployment Guide - AI Document Classifier Backend

Complete guide for deploying the backend to production.

## Pre-Deployment Checklist

- [ ] All code committed to git
- [ ] `.env` file configured for production
- [ ] JWT_SECRET changed to strong secret
- [ ] MONGODB_URI points to production database
- [ ] ML_SERVICE_URL points to production service
- [ ] CLIENT_URL configured
- [ ] NODE_ENV set to "production"
- [ ] Error logs configured
- [ ] CORS domains verified

## Environment Variables (Production)

Create `.env` for production:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/ai-document-classifier

# JWT Configuration (Use strong secret!)
JWT_SECRET=your_very_secure_jwt_secret_key_minimum_32_characters_long
JWT_EXPIRE=7d

# Server Configuration
PORT=5000
NODE_ENV=production

# Python ML Service Configuration
ML_SERVICE_URL=https://ml-service.yourdomain.com/classify

# File Upload Configuration
MAX_FILE_SIZE=10485760
UPLOAD_TEMP_DIR=./uploads/temp

# Client Configuration
CLIENT_URL=https://yourdomain.com
```

## Deployment Options

### Option 1: Heroku Deployment

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set JWT_SECRET=your_secret
   heroku config:set MONGODB_URI=your_mongodb_uri
   heroku config:set NODE_ENV=production
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View Logs**
   ```bash
   heroku logs --tail
   ```

### Option 2: DigitalOcean App Platform

1. **Connect Repository**
   - Go to DigitalOcean App Platform
   - Select your GitHub repository
   - Choose the `server` directory

2. **Set Environment Variables**
   - In App Platform dashboard, add all production `.env` variables

3. **Deploy**
   - Push to main branch or deploy manually
   - DigitalOcean automatically builds and deploys

### Option 3: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli --upgrade --user
   ```

2. **Initialize Application**
   ```bash
   eb init -p "Node.js 18 running on 64bit Amazon Linux 2" ai-classifier
   eb create production-env
   ```

3. **Set Environment Variables**
   ```bash
   eb setenv JWT_SECRET=your_secret MONGODB_URI=your_uri NODE_ENV=production
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

5. **View Logs**
   ```bash
   eb logs
   ```

### Option 4: Self-Hosted (VPS/Server)

1. **SSH into Server**
   ```bash
   ssh user@your_server_ip
   ```

2. **Install Node.js & MongoDB**
   ```bash
   curl -sL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

3. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/ai-document-classifier.git
   cd ai-document-classifier/server
   ```

4. **Install Dependencies**
   ```bash
   npm install --production
   ```

5. **Create .env File**
   ```bash
   nano .env
   # Add all production environment variables
   ```

6. **Use PM2 for Process Management**
   ```bash
   sudo npm install -g pm2
   pm2 start server.js --name "ai-classifier"
   pm2 startup
   pm2 save
   ```

7. **Set Up Nginx Reverse Proxy**
   ```bash
   sudo apt-get install nginx
   ```

   Edit `/etc/nginx/sites-available/default`:
   ```nginx
   server {
     listen 80;
     server_name yourdomain.com;

     location / {
       proxy_pass http://localhost:5000;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection 'upgrade';
       proxy_set_header Host $host;
       proxy_cache_bypass $http_upgrade;
     }
   }
   ```

   Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

8. **Enable HTTPS with Let's Encrypt**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ```

## MongoDB Setup (Production)

### Option 1: MongoDB Atlas (Recommended)

1. **Sign Up at MongoDB Atlas**: https://www.mongodb.com/cloud/atlas
2. **Create Cluster**: Free tier available
3. **Get Connection String**: 
   ```
   mongodb+srv://user:password@cluster.mongodb.net/ai-document-classifier
   ```
4. **Configure Firewall**: Allow your server IP

### Option 2: Self-Hosted MongoDB

1. **Install MongoDB**
   ```bash
   sudo apt-get install -y mongodb-org
   ```

2. **Enable Authentication**
   ```bash
   # Create admin user
   mongosh
   > use admin
   > db.createUser({user: "admin", pwd: "password", roles: ["root"]})
   ```

3. **Connection String**
   ```
   mongodb://admin:password@localhost:27017/ai-document-classifier?authSource=admin
   ```

4. **Backup Strategy**
   ```bash
   # Daily backup
   mongodump --out /backup/$(date +\%Y-\%m-\%d)
   ```

## SSL/HTTPS Configuration

### Using Let's Encrypt with Nginx

```bash
sudo certbot certonly --nginx -d yourdomain.com
```

Update Nginx config:
```nginx
server {
  listen 443 ssl;
  server_name yourdomain.com;

  ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

  location / {
    proxy_pass http://localhost:5000;
  }
}

# Redirect HTTP to HTTPS
server {
  listen 80;
  server_name yourdomain.com;
  return 301 https://$server_name$request_uri;
}
```

Auto-renewal:
```bash
sudo certbot renew --dry-run
```

## Performance Optimization

### 1. Enable Compression
Add to `server.js`:
```javascript
const compression = require('compression');
app.use(compression());
```

### 2. Add Caching Headers
```javascript
app.use((req, res, next) => {
  res.set('Cache-Control', 'public, max-age=3600');
  next();
});
```

### 3. Use Redis for Session Caching
```bash
npm install redis express-session connect-redis
```

### 4. Database Query Optimization
- Use indexes (already configured)
- Implement query pagination
- Use `.lean()` for read-only queries

### 5. Load Balancing (nginx)
```nginx
upstream backend {
  server localhost:5000;
  server localhost:5001;
  server localhost:5002;
}

server {
  listen 80;
  location / {
    proxy_pass http://backend;
  }
}
```

## Monitoring & Logging

### Using PM2 Monitoring
```bash
pm2 install pm2-logrotate
pm2 monit
```

### Using Winston Logger
```bash
npm install winston
```

Add to `server.js`:
```javascript
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
  ],
});
```

### Health Check Endpoint
Already implemented:
```
GET /health
```

Monitor with:
```bash
watch -n 5 'curl http://yourdomain.com/health'
```

## Backup & Recovery

### Database Backups
```bash
# Backup MongoDB
mongodump --uri "mongodb+srv://user:pass@cluster.mongodb.net/ai-document-classifier" --out ./backup

# Restore MongoDB
mongorestore --uri "mongodb+srv://user:pass@cluster.mongodb.net/ai-document-classifier" ./backup
```

### Automated Backup Script
Create `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +\%Y-\%m-\%d_%H-%M-%S)
mongodump --uri "mongodb+srv://user:pass@cluster.mongodb.net/ai-document-classifier" \
  --out "./backups/backup_$DATE"
tar -czf "./backups/backup_$DATE.tar.gz" "./backups/backup_$DATE"
rm -rf "./backups/backup_$DATE"
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

## Security Best Practices

1. **Environment Variables**
   - Never commit `.env` to git
   - Use strong, unique JWT_SECRET
   - Rotate secrets regularly

2. **CORS Configuration**
   - Whitelist specific domains only
   - Never use wildcard (*) in production

3. **Rate Limiting**
   ```bash
   npm install express-rate-limit
   ```

4. **Security Headers**
   ```bash
   npm install helmet
   ```

   Add to `server.js`:
   ```javascript
   const helmet = require('helmet');
   app.use(helmet());
   ```

5. **Input Validation**
   - Already implemented with validators
   - Add additional validation as needed

6. **SQL/Injection Prevention**
   - Use Mongoose (prevents injection)
   - Validate all user inputs

7. **HTTPS Only**
   - Redirect HTTP to HTTPS
   - Use secure cookies

## Scaling Strategies

1. **Horizontal Scaling**
   - Multiple server instances
   - Load balancer (nginx, AWS ELB)
   - Shared database (MongoDB Atlas)

2. **Vertical Scaling**
   - Increase server resources (CPU, RAM)
   - Optimize database queries
   - Enable caching

3. **Database Optimization**
   - Add read replicas
   - Enable sharding for large datasets
   - Regular index maintenance

## Troubleshooting

### Issue: High Memory Usage
**Solution:**
```bash
node --max-old-space-size=4096 server.js
```

### Issue: Connection Timeouts
**Solution:** Increase timeout in `server.js`:
```javascript
server.setTimeout(60000); // 60 seconds
```

### Issue: Database Slow Queries
**Solution:**
```javascript
// Enable query logging in MongoDB
mongoose.set('debug', true);
```

### Issue: SSL Certificate Error
**Solution:**
```bash
sudo certbot renew --force-renewal
sudo systemctl restart nginx
```

## Monitoring Tools

- **PM2 Plus**: https://pm2.io/runtime/
- **New Relic**: https://newrelic.com/
- **Datadog**: https://www.datadoghq.com/
- **Sentry**: https://sentry.io/

## Rollback Procedure

1. **Keep Previous Version**
   ```bash
   git log
   git checkout <previous-commit>
   npm install
   npm start
   ```

2. **Using PM2**
   ```bash
   pm2 list
   pm2 restart ai-classifier
   ```

3. **Database Rollback**
   ```bash
   mongorestore --uri "mongodb+srv://..." ./backup/previous_date
   ```

## Production Checklist

- [ ] Error logging configured
- [ ] Monitoring active
- [ ] Backups automated
- [ ] SSL/HTTPS enabled
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] Health check working
- [ ] Firewall rules set
- [ ] Database credentials secured
- [ ] JWT secret strong and unique
- [ ] Load testing completed
- [ ] Rollback plan tested

---

For questions or issues, refer to deployment-specific documentation or contact your hosting provider support.
