FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy library to system location
# Note: libdmcompverify.so should be in the same directory as Dockerfile
COPY libdmcompverify.so /usr/lib/libdmcompverify.so
RUN chmod 644 /usr/lib/libdmcompverify.so && \
    ldconfig

# Copy application files
COPY main.py requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "8000"]

