# Deployment Guide

## 🐳 Docker Deployment (Recommended)

### Quick Start

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/dmcompverify-api.git
cd dmcompverify-api

# Start with Docker Compose (easiest)
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

### Manual Docker Build

```bash
# Build image
docker build -t dmcompverify-api .

# Run container
docker run -d \
  --name dmcompverify-api \
  -p 8000:8000 \
  --restart unless-stopped \
  dmcompverify-api

# View logs
docker logs -f dmcompverify-api
```

## 🖥️ VPS Deployment

### Option 1: Docker on VPS

```bash
# On VPS
git clone https://github.com/YOUR_USERNAME/dmcompverify-api.git
cd dmcompverify-api
docker-compose up -d
```

### Option 2: Direct Python on VPS

```bash
# On VPS
git clone https://github.com/YOUR_USERNAME/dmcompverify-api.git
cd dmcompverify-api

# Copy library
sudo cp libdmcompverify.so /usr/lib/
sudo chmod 644 /usr/lib/libdmcompverify.so
sudo ldconfig

# Install dependencies
pip3 install -r requirements.txt

# Run
python3 main.py
```

## ☁️ Cloud Provider Deployment

### AWS EC2

1. Launch EC2 instance (Ubuntu 22.04)
2. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. Clone and run:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dmcompverify-api.git
   cd dmcompverify-api
   docker-compose up -d
   ```

### DigitalOcean Droplet

1. Create Droplet (Ubuntu 22.04)
2. Install Docker (same as AWS)
3. Clone and run (same as AWS)

### Google Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR_PROJECT/dmcompverify-api

# Deploy
gcloud run deploy dmcompverify-api \
  --image gcr.io/YOUR_PROJECT/dmcompverify-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## 🔧 Systemd Service (Linux)

Create `/etc/systemd/system/dmcompverify-api.service`:

```ini
[Unit]
Description=DMCompVerify API Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/dmcompverify-api
ExecStart=/usr/bin/python3 /opt/dmcompverify-api/main.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10
Environment="LIBDMCOMPVERIFY_PATH=/usr/lib/libdmcompverify.so"

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable dmcompverify-api
sudo systemctl start dmcompverify-api
sudo systemctl status dmcompverify-api
```

## 🔒 Security Setup

### Firewall (UFW)

```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Or restrict to specific IP
sudo ufw allow from YOUR_IP to any port 8000
```

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### SSL with Let's Encrypt

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

## 📊 Monitoring

### Health Check

```bash
# Check health
curl http://your-vps-ip:8000/health

# Or with Docker
docker exec dmcompverify-api curl http://localhost:8000/health
```

### Logs

```bash
# Docker logs
docker-compose logs -f

# Systemd logs
journalctl -u dmcompverify-api -f
```

## 🔄 Updates

### Update with Docker

```bash
cd dmcompverify-api
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

### Update with Systemd

```bash
cd /opt/dmcompverify-api
git pull
sudo systemctl restart dmcompverify-api
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Check if library exists
docker exec dmcompverify-api ls -la /usr/lib/libdmcompverify.so
```

### Library Not Found

```bash
# Verify library is in Docker image
docker run --rm dmcompverify-api ls -la /usr/lib/libdmcompverify.so

# Rebuild if needed
docker-compose build --no-cache
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process or change port
docker-compose.yml: ports: "8001:8000"
```

