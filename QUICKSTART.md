# Quick Start Guide

## 🚀 Deploy to VPS in 3 Steps

### Step 1: Copy Files to VPS

```bash
# On your local machine, copy the API folder
scp -r dmcompverify_api/ user@vps-ip:/opt/dmcompverify_api/

# Copy the library file
scp neurons/executor/libdmcompverify.so user@vps-ip:/usr/lib/libdmcompverify.so
```

### Step 2: Install Dependencies on VPS

```bash
# SSH into VPS
ssh user@vps-ip

# Navigate to API directory
cd /opt/dmcompverify_api

# Install Python dependencies
pip3 install -r requirements.txt
```

### Step 3: Run the API

```bash
# Run directly
python3 main.py

# Or run in background
nohup python3 main.py > api.log 2>&1 &

# Or with custom port
python3 main.py --port 8001
```

## ✅ Test the API

```bash
# Health check
curl http://vps-ip:8000/health

# Process a challenge
curl -X POST http://vps-ip:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "dim_n": 1981,
    "dim_k": 1555929,
    "seed": 1743502434,
    "cipher_text": "e28702c2f187f34d56744d64a4399e00cbecbde2d3f6ca53a8abec5cbc40481d42a1a505"
  }'
```

## 🔧 Systemd Service (Optional)

Create `/etc/systemd/system/dmcompverify-api.service`:

```ini
[Unit]
Description=DMCompVerify API Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/opt/dmcompverify_api
ExecStart=/usr/bin/python3 /opt/dmcompverify_api/main.py --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl start dmcompverify-api
sudo systemctl enable dmcompverify-api
```

## 📝 That's It!

Your API is now running and ready to process challenges!

