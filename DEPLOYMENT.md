# TalentScout Hiring Assistant - Deployment Guide

This guide covers deploying the TalentScout Hiring Assistant to various cloud platforms.

## Table of Contents

1. [Streamlit Cloud](#streamlit-cloud)
2. [AWS Deployment](#aws-deployment)
3. [Google Cloud Platform](#google-cloud-platform)
4. [Azure Deployment](#azure-deployment)
5. [Docker Deployment](#docker-deployment)

---

## Streamlit Cloud

Streamlit Cloud is the easiest way to deploy Streamlit apps.

### Prerequisites

- GitHub account with the repository pushed
- Streamlit Community Cloud account

### Deployment Steps

1. **Push to GitHub**

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Sign in to Streamlit Cloud**

Visit [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.

3. **Deploy Your App**

- Click "New app"
- Select your repository
- Select branch: `main`
- Select file: `streamlit_app.py`
- Click "Deploy"

4. **Configure Secrets**

In Streamlit Cloud settings, add your secrets:

```
[secrets]
OPENAI_API_KEY = "your-api-key-here"
DATA_SALT = "your-salt-here"
```

5. **Share Your Link**

Your app will be available at:
```
https://<username>-talentscout.streamlit.app/
```

### Troubleshooting

**App won't load**: Check logs for errors
**API errors**: Verify OPENAI_API_KEY is set correctly
**Data not saving**: Check file write permissions

---

## AWS Deployment

### Option 1: AWS Elastic Beanstalk

#### Prerequisites

- AWS account
- AWS CLI configured
- Docker installed

#### Steps

1. **Create Dockerized Application**

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Create .dockerignore**

```
venv/
.git/
.gitignore
__pycache__/
*.pyc
.pytest_cache/
.env
data/
```

3. **Initialize EB**

```bash
pip install awseb-cli
eb init -p "Docker running on 64bit Amazon Linux 2" --region us-east-1
```

4. **Create Environment Configuration**

Create `.elasticbeanstalk/config.yml`:

```yaml
branch-defaults:
  main:
    environment: talentscout-prod

environment-defaults:
  talentscout-prod:
    branch: main

global:
  application_name: talentscout
  default_region: us-east-1
  default_platform: Docker running on 64bit Amazon Linux 2
  include_git_submodules: true
  instance_profile: null
  platform_name: null
  platform_version: null
  sc: git
```

5. **Deploy**

```bash
eb create talentscout-prod
eb deploy
```

6. **Configure Environment Variables**

```bash
eb setenv OPENAI_API_KEY=your-api-key
eb setenv DATA_SALT=your-salt
```

7. **Monitor and Access**

```bash
eb status
eb open
```

### Option 2: AWS EC2 Direct

1. **Launch EC2 Instance**

- AMI: Ubuntu 20.04 LTS
- Instance type: t3.micro (free tier)
- Security group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect via SSH**

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. **Install Dependencies**

```bash
sudo apt update
sudo apt install python3-pip python3-venv git -y

git clone <your-repo-url>
cd "Talent Scout Hiring Assistant"

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Set Up Environment**

```bash
nano .env
# Add your API key
```

5. **Run with Systemd**

Create `/etc/systemd/system/talentscout.service`:

```ini
[Unit]
Description=TalentScout Hiring Assistant
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Talent Scout Hiring Assistant
Environment="PATH=/home/ubuntu/Talent Scout Hiring Assistant/venv/bin"
ExecStart=/home/ubuntu/Talent Scout Hiring Assistant/venv/bin/streamlit run streamlit_app.py --server.port 80 --server.address 0.0.0.0

Restart=always

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start talentscout
sudo systemctl enable talentscout
```

---

## Google Cloud Platform

### Cloud Run Deployment

1. **Create Dockerfile** (see AWS section)

2. **Build and Push to Container Registry**

```bash
gcloud auth configure-docker
docker build -t gcr.io/your-project/talentscout:latest .
docker push gcr.io/your-project/talentscout:latest
```

3. **Deploy to Cloud Run**

```bash
gcloud run deploy talentscout \
  --image gcr.io/your-project/talentscout:latest \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=your-api-key \
  --set-env-vars DATA_SALT=your-salt \
  --memory 512Mi \
  --timeout 3600
```

4. **Access Your App**

```
https://talentscout-<random-id>.run.app
```

### App Engine Deployment

1. **Create app.yaml**

```yaml
runtime: python39

env: standard

entrypoint: streamlit run streamlit_app.py --server.port 8080 --server.address 0.0.0.0

env_variables:
  OPENAI_API_KEY: "your-api-key"
  DATA_SALT: "your-salt"
```

2. **Deploy**

```bash
gcloud app deploy
```

---

## Azure Deployment

### App Service Deployment

1. **Install Azure CLI**

```bash
# Windows
choco install azure-cli

# macOS
brew install azure-cli

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

2. **Login and Create Resources**

```bash
az login
az group create --name talentscout --location eastus
```

3. **Create App Service**

```bash
az appservice plan create \
  --name talentscout-plan \
  --resource-group talentscout \
  --sku B1 --is-linux

az webapp create \
  --resource-group talentscout \
  --plan talentscout-plan \
  --name talentscout-app \
  --runtime "python|3.9"
```

4. **Configure and Deploy**

```bash
az webapp config appsettings set \
  --resource-group talentscout \
  --name talentscout-app \
  --settings OPENAI_API_KEY=your-api-key DATA_SALT=your-salt

# Deploy from local
az webapp up --name talentscout-app --resource-group talentscout
```

---

## Docker Deployment

### Local Docker

1. **Build Image**

```bash
docker build -t talentscout:latest .
```

2. **Run Container**

```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your-api-key \
  -e DATA_SALT=your-salt \
  talentscout:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  talentscout:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATA_SALT=${DATA_SALT}
    volumes:
      - ./data:/app/data

volumes:
  data:
```

Run:

```bash
docker-compose up
```

---

## Performance Optimization

### For Production

1. **Use CDN for Static Assets**
   - CloudFront (AWS)
   - Cloud CDN (GCP)
   - Azure CDN

2. **Enable Caching**
   - Add cache headers
   - Use Redis for session storage

3. **Monitor Performance**
   - Enable application monitoring
   - Set up alerts
   - Track API usage

4. **Auto-scaling**
   - Configure auto-scaling policies
   - Monitor load metrics

### Streamlit-Specific

```python
@st.cache_data
def load_model():
    # Cache expensive operations
    pass

@st.cache_resource
def init_llm():
    # Cache connection to LLM
    pass
```

---

## Cost Estimation

| Platform | Tier | Monthly Cost | Notes |
|----------|------|------------|-------|
| Streamlit Cloud | Free | $0 | Good for testing |
| Streamlit Cloud | Pro | $15+ | Includes priority support |
| AWS EC2 | t3.micro | $10 | Free tier eligible |
| Google Cloud Run | Standard | $0.20 per 1M requests | Pay-as-you-go |
| Azure App Service | B1 | $12.50 | Cheapest tier |

---

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Enable HTTPS** - Use SSL/TLS certificates
3. **Rate limiting** - Protect API endpoints
4. **Input validation** - Sanitize all inputs
5. **Monitor logs** - Track unusual activity
6. **Update dependencies** - Keep packages current
7. **Regular backups** - Back up candidate data

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Port already in use | Change port: `--server.port 8502` |
| Memory error | Increase instance memory |
| API timeout | Increase timeout settings |
| CORS errors | Configure CORS headers |
| Data not persisting | Use cloud storage (S3, GCS) |

### Debug Logs

```bash
# Streamlit logs
streamlit logs

# Docker logs
docker logs container-name

# Cloud logs
# AWS: CloudWatch
# GCP: Cloud Logging
# Azure: Application Insights
```

---

## Support

For deployment issues:
- Check cloud platform documentation
- Review application logs
- Verify environment variables
- Test locally first

---

**Last Updated**: November 2024
