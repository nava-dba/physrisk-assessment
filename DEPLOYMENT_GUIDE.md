# 🚀 Deployment Guide - Share Your PhysRisk App Globally

## Overview

This guide shows you how to deploy your PhysRisk web application so users worldwide can access it through a URL, without needing to install anything.

---

## 🌟 Deployment Options

### Option 1: Streamlit Cloud (EASIEST) ⭐ **RECOMMENDED**
- ✅ **Free** for public apps
- ✅ **No server management**
- ✅ **Automatic updates** from GitHub
- ✅ **Custom domain** support
- ✅ **Deploy in 5 minutes**

### Option 2: Heroku
- ✅ Free tier available
- ✅ Easy deployment
- ✅ Good for small teams

### Option 3: AWS/Google Cloud/Azure
- ✅ Full control
- ✅ Scalable
- ✅ Enterprise-grade
- ⚠️ Requires more setup

### Option 4: Docker + Any Cloud
- ✅ Portable
- ✅ Consistent environment
- ✅ Works anywhere

---

## 🎯 Option 1: Streamlit Cloud (Recommended)

### Step 1: Prepare Your Code

1. **Create a GitHub account** (if you don't have one)
   - Go to https://github.com
   - Sign up for free

2. **Create a new repository**
   - Click "New repository"
   - Name it: `physrisk-assessment`
   - Make it Public (for free hosting)
   - Click "Create repository"

3. **Upload your files to GitHub**

```bash
# In your BDO directory
cd /Users/nava/Documents/BDO

# Initialize git (if not already done)
git init

# Add all files
git add app.py
git add physrisk_pipeline_v2.py
git add requirements.txt
git add *.md

# Commit
git commit -m "Initial commit - PhysRisk Assessment App"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/physrisk-assessment.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://streamlit.io/cloud
   - Click "Sign up" (use your GitHub account)

2. **Create New App**
   - Click "New app"
   - Select your repository: `physrisk-assessment`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Wait for Deployment** (2-3 minutes)
   - Streamlit will install dependencies
   - Build your app
   - Generate a URL

4. **Get Your URL**
   - You'll get a URL like: `https://your-app-name.streamlit.app`
   - Share this URL with anyone!

### Step 3: Configure Settings (Optional)

In Streamlit Cloud dashboard:
- **Custom domain**: Add your own domain
- **Secrets**: Add API keys securely
- **Resources**: Upgrade for more power
- **Analytics**: Track usage

### Step 4: Update Your App

Whenever you update your code:
```bash
git add .
git commit -m "Update description"
git push
```

Streamlit Cloud will automatically redeploy!

---

## 🎯 Option 2: Heroku Deployment

### Step 1: Prepare Files

Create `Procfile` in your project directory:

```bash
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `runtime.txt`:

```
python-3.9.18
```

Update `requirements.txt` to include:

```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
openpyxl>=3.1.0
requests>=2.31.0
numpy>=1.24.0
```

### Step 2: Deploy to Heroku

```bash
# Install Heroku CLI
# Mac: brew install heroku/brew/heroku
# Windows: Download from https://devcenter.heroku.com/articles/heroku-cli

# Login to Heroku
heroku login

# Create app
heroku create physrisk-assessment

# Deploy
git push heroku main

# Open app
heroku open
```

Your app will be at: `https://physrisk-assessment.herokuapp.com`

---

## 🎯 Option 3: Docker Deployment

### Step 1: Create Dockerfile

Create `Dockerfile` in your project:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  physrisk-app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_ENABLE_CORS=false
    restart: unless-stopped
```

### Step 3: Build and Run

```bash
# Build image
docker build -t physrisk-app .

# Run container
docker run -p 8501:8501 physrisk-app

# Or use docker-compose
docker-compose up -d
```

### Step 4: Deploy to Cloud

**AWS ECS:**
```bash
# Push to ECR
aws ecr create-repository --repository-name physrisk-app
docker tag physrisk-app:latest YOUR_ECR_URL/physrisk-app:latest
docker push YOUR_ECR_URL/physrisk-app:latest

# Deploy to ECS (use AWS Console or CLI)
```

**Google Cloud Run:**
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT/physrisk-app
gcloud run deploy physrisk-app --image gcr.io/YOUR_PROJECT/physrisk-app --platform managed
```

**Azure Container Instances:**
```bash
# Create container
az container create \
  --resource-group myResourceGroup \
  --name physrisk-app \
  --image YOUR_REGISTRY/physrisk-app:latest \
  --dns-name-label physrisk-app \
  --ports 8501
```

---

## 🎯 Option 4: AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Launch Instance:
   - AMI: Ubuntu 22.04
   - Instance type: t2.medium (or larger)
   - Security group: Allow ports 22 (SSH) and 8501 (Streamlit)

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone your repository
git clone https://github.com/YOUR_USERNAME/physrisk-assessment.git
cd physrisk-assessment

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

### Step 3: Setup as Service

Create `/etc/systemd/system/physrisk.service`:

```ini
[Unit]
Description=PhysRisk Assessment App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/physrisk-assessment
Environment="PATH=/home/ubuntu/physrisk-assessment/venv/bin"
ExecStart=/home/ubuntu/physrisk-assessment/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable physrisk
sudo systemctl start physrisk
sudo systemctl status physrisk
```

### Step 4: Setup Domain and SSL

```bash
# Install Nginx
sudo apt install nginx -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y

# Configure Nginx
sudo nano /etc/nginx/sites-available/physrisk
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable and get SSL:
```bash
sudo ln -s /etc/nginx/sites-available/physrisk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo certbot --nginx -d your-domain.com
```

---

## 🔐 Security Best Practices

### 1. Add Authentication

Install streamlit-authenticator:
```bash
pip install streamlit-authenticator
```

Update `app.py`:
```python
import streamlit_authenticator as stauth

# Configuration
names = ['John Doe', 'Jane Smith']
usernames = ['jdoe', 'jsmith']
passwords = ['password123', 'password456']  # Use hashed passwords in production

# Create authenticator
hashed_passwords = stauth.Hasher(passwords).generate()
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    'physrisk_cookie',
    'physrisk_key',
    cookie_expiry_days=30
)

# Login
name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    # Your app code here
    main()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
```

### 2. Environment Variables

Create `.streamlit/secrets.toml`:
```toml
[api]
physrisk_key = "your-api-key"
openai_key = "your-openai-key"

[database]
connection_string = "your-db-connection"
```

Access in code:
```python
import streamlit as st

api_key = st.secrets["api"]["physrisk_key"]
```

### 3. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(max_calls=10, time_window=60):
    calls = []
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            calls[:] = [c for c in calls if c > now - time_window]
            
            if len(calls) >= max_calls:
                st.error("Rate limit exceeded. Please try again later.")
                return None
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=5, time_window=60)
def process_data():
    # Your processing code
    pass
```

---

## 📊 Monitoring and Analytics

### 1. Google Analytics

Add to `app.py`:
```python
import streamlit.components.v1 as components

# Google Analytics
ga_code = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
"""

components.html(ga_code, height=0)
```

### 2. Application Logging

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename=f'app_usage_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Log events
logging.info(f"User uploaded file: {filename}")
logging.info(f"Processing completed: {asset_count} assets")
logging.error(f"Error occurred: {error_message}")
```

### 3. Performance Monitoring

```python
import time

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        
        logging.info(f"{func.__name__} took {elapsed:.2f} seconds")
        
        if elapsed > 10:
            st.warning(f"Processing took {elapsed:.2f} seconds. Consider optimizing.")
        
        return result
    return wrapper

@monitor_performance
def process_large_dataset(data):
    # Your processing code
    pass
```

---

## 💰 Cost Estimates

### Streamlit Cloud
- **Free**: Public apps, 1GB resources
- **Pro**: $20/month, private apps, 4GB resources
- **Enterprise**: Custom pricing

### Heroku
- **Free**: 550 hours/month (with credit card)
- **Hobby**: $7/month
- **Standard**: $25-50/month

### AWS EC2
- **t2.micro**: Free tier (1 year)
- **t2.medium**: ~$35/month
- **t2.large**: ~$70/month

### Google Cloud Run
- **Free tier**: 2 million requests/month
- **Paid**: $0.00002400 per request

### Azure
- **Free tier**: 1 million requests/month
- **Paid**: Similar to Google Cloud

---

## 🎯 Quick Comparison

| Feature | Streamlit Cloud | Heroku | AWS EC2 | Docker |
|---------|----------------|--------|---------|--------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Cost (Small)** | Free | $7/mo | $35/mo | Varies |
| **Scalability** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Maintenance** | None | Low | Medium | Medium |
| **Custom Domain** | ✅ | ✅ | ✅ | ✅ |
| **SSL/HTTPS** | Auto | Auto | Manual | Manual |
| **Best For** | Quick start | Small teams | Enterprise | Flexibility |

---

## 📝 Deployment Checklist

### Before Deployment
- [ ] Test app locally
- [ ] Update requirements.txt
- [ ] Add .gitignore file
- [ ] Remove sensitive data
- [ ] Add authentication (if needed)
- [ ] Test with sample data
- [ ] Optimize performance
- [ ] Add error handling

### During Deployment
- [ ] Choose deployment platform
- [ ] Setup repository (GitHub)
- [ ] Configure environment variables
- [ ] Deploy application
- [ ] Test deployed app
- [ ] Setup custom domain (optional)
- [ ] Enable SSL/HTTPS
- [ ] Configure monitoring

### After Deployment
- [ ] Share URL with users
- [ ] Monitor performance
- [ ] Check logs regularly
- [ ] Gather user feedback
- [ ] Plan updates
- [ ] Setup backup strategy
- [ ] Document for team

---

## 🚀 Recommended Deployment Path

### For Quick Start (5 minutes):
1. **Push to GitHub**
2. **Deploy to Streamlit Cloud**
3. **Share URL**

### For Production (1 hour):
1. **Setup GitHub repository**
2. **Add authentication**
3. **Deploy to Streamlit Cloud or AWS**
4. **Configure custom domain**
5. **Enable monitoring**
6. **Document for team**

---

## 📞 Support Resources

### Streamlit Cloud
- Docs: https://docs.streamlit.io/streamlit-community-cloud
- Forum: https://discuss.streamlit.io

### Heroku
- Docs: https://devcenter.heroku.com
- Support: https://help.heroku.com

### AWS
- Docs: https://docs.aws.amazon.com
- Support: AWS Support Center

### Docker
- Docs: https://docs.docker.com
- Hub: https://hub.docker.com

---

## 🎉 You're Ready to Deploy!

**Recommended for beginners:**
```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git push origin main

# 2. Go to streamlit.io/cloud
# 3. Click "New app"
# 4. Select your repo
# 5. Deploy!
```

**Your app will be live at:**
`https://your-app-name.streamlit.app`

**Share this URL with anyone in the world!** 🌍

---

**Questions?** Check the platform-specific documentation or reach out to their support teams.

**Happy deploying!** 🚀