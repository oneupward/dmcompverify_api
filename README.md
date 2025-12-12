# DMCompVerify API

🚀 **Standalone API server for processing DMCompVerify challenges**

A simple, production-ready FastAPI application that processes DMCompVerify matrix multiplication challenges. Perfect for deploying on any VPS or cloud provider.

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

## ✨ Features

- 🐳 **Docker-ready** - One command deployment
- 🚀 **Fast & Lightweight** - Minimal dependencies
- 🔒 **Production-ready** - Health checks, error handling
- 📡 **RESTful API** - Simple HTTP interface
- 🔧 **Easy to Deploy** - Works on any VPS or cloud provider

## 🚀 Quick Start with Docker

### Prerequisites

- Docker and Docker Compose installed
- `libdmcompverify.so` file (included in repository)

### Run with Docker Compose

```bash
# Clone the repository
git clone https://github.com/yourusername/dmcompverify-api.git
cd dmcompverify-api

# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Run with Docker

```bash
# Build the image
docker build -t dmcompverify-api .

# Run the container
docker run -d \
  --name dmcompverify-api \
  -p 8000:8000 \
  --restart unless-stopped \
  dmcompverify-api

# Check status
docker ps
docker logs dmcompverify-api
```

## 📡 API Endpoints

### Health Check

```bash
GET http://localhost:8000/health
```

**Response:**
```json
{
    "status": "healthy",
    "library_loaded": true
}
```

### Process Challenge

```bash
POST http://localhost:8000/process
Content-Type: application/json

{
    "dim_n": 1981,
    "dim_k": 1555929,
    "seed": 1743502434,
    "cipher_text": "e28702c2f187f34d56744d64a4399e00cbecbde2d3f6ca53a8abec5cbc40481d42a1a505"
}
```

**Response:**
```json
{
    "uuid": "extracted-uuid-here",
    "success": true,
    "message": "Challenge processed successfully"
}
```

## 🛠️ Manual Installation

### Step 1: Copy Library

```bash
# Copy libdmcompverify.so to system location
sudo cp libdmcompverify.so /usr/lib/libdmcompverify.so
sudo chmod 644 /usr/lib/libdmcompverify.so
sudo ldconfig
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the API

```bash
# Basic run
python main.py

# Custom port
python main.py --port 8001

# Custom library path
python main.py --lib-path /custom/path/libdmcompverify.so
```

## 📋 Configuration

### Environment Variables

- `LIBDMCOMPVERIFY_PATH` - Path to `libdmcompverify.so` (default: `/usr/lib/libdmcompverify.so`)

### Command Line Arguments

```bash
python main.py --help

Options:
  --host TEXT     Host to bind to [default: 0.0.0.0]
  --port INTEGER  Port to bind to [default: 8000]
  --lib-path TEXT Path to libdmcompverify.so [default: /usr/lib/libdmcompverify.so]
```

## 🔄 Integration Example

### Python Client

```python
import requests

def process_challenge(api_url: str, dim_n: int, dim_k: int, seed: int, cipher_text: str):
    response = requests.post(
        f"{api_url}/process",
        json={
            "dim_n": dim_n,
            "dim_k": dim_k,
            "seed": seed,
            "cipher_text": cipher_text
        }
    )
    response.raise_for_status()
    return response.json()

# Usage
result = process_challenge(
    api_url="http://your-vps-ip:8000",
    dim_n=1981,
    dim_k=1555929,
    seed=1743502434,
    cipher_text="your_cipher_text_here"
)
print(f"UUID: {result['uuid']}")
```

### cURL

```bash
curl -X POST http://your-vps-ip:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "dim_n": 1981,
    "dim_k": 1555929,
    "seed": 1743502434,
    "cipher_text": "your_cipher_text_here"
  }'
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t dmcompverify-api .
```

### Run Container

```bash
docker run -d \
  --name dmcompverify-api \
  -p 8000:8000 \
  --restart unless-stopped \
  dmcompverify-api
```

### Docker Compose

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔒 Security Considerations

1. **Firewall**: Restrict access to trusted IPs only
2. **HTTPS**: Use reverse proxy (nginx) with SSL for production
3. **Authentication**: Add API key or signature verification if needed
4. **Rate Limiting**: Consider adding rate limiting to prevent abuse

### Example: Nginx Reverse Proxy

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📁 Project Structure

```
dmcompverify-api/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Docker Compose configuration
├── libdmcompverify.so     # DMCompVerify library
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### Process Challenge

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "dim_n": 1981,
    "dim_k": 1555929,
    "seed": 1743502434,
    "cipher_text": "e28702c2f187f34d56744d64a4399e00cbecbde2d3f6ca53a8abec5cbc40481d42a1a505"
  }'
```

## 🛠️ Troubleshooting

### Library Not Found

**Error:** `Library not found: /usr/lib/libdmcompverify.so`

**Solution:**
```bash
# Ensure library is in correct location
sudo cp libdmcompverify.so /usr/lib/
sudo ldconfig
```

### Permission Denied

**Error:** `Permission denied`

**Solution:**
```bash
sudo chmod 644 /usr/lib/libdmcompverify.so
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use different port
python main.py --port 8001

# Or in Docker
docker run -p 8001:8000 dmcompverify-api
```

## 📦 Dependencies

- `fastapi==0.110.3` - Web framework
- `uvicorn==0.34.0` - ASGI server
- `pydantic==2.10.6` - Data validation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Projects

- [Bittensor Subnet 51](https://github.com/Datura-ai/lium-io) - Main project

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for the Bittensor community**
