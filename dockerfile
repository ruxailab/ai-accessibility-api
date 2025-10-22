# Production-grade Dockerfile for FastAPI on Cloud Run
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies for Chrome/Playwright and general tooling
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libuuid1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome Stable (for Selenium/Axe)
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    wget -O /tmp/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_${arch}.deb" || \
    wget -O /tmp/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"; \
    apt-get update; \
    apt-get install -y /tmp/google-chrome.deb; \
    rm -rf /var/lib/apt/lists/* /tmp/google-chrome.deb

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install chromium

# Copy application code
COPY . .

# Create non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app && chown -R app:app /app
USER app

# Cloud Run will set PORT; default to 8080
ENV PORT=8080

# Ensure Chrome binaries are discoverable
ENV GOOGLE_CHROME_SHIM=/usr/bin/google-chrome \
    CHROME_BIN=/usr/bin/google-chrome

EXPOSE 8080

# Start the FastAPI app with uvicorn, binding to Cloud Run's PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
# Production-grade Dockerfile for FastAPI on Cloud Run
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System dependencies for Chrome/Playwright and general tooling
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libc6 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libexpat1 \
    libfontconfig1 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libuuid1 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome Stable (for Selenium/Axe)
RUN set -eux; \
    arch="$(dpkg --print-architecture)"; \
    wget -O /tmp/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_${arch}.deb" || \
    wget -O /tmp/google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"; \
    apt-get update; \
    apt-get install -y /tmp/google-chrome.deb; \
    rm -rf /var/lib/apt/lists/* /tmp/google-chrome.deb

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m playwright install chromium

# Copy application code
COPY . .

# Create non-root user for security
RUN addgroup --system app && adduser --system --ingroup app app && chown -R app:app /app
USER app

# Cloud Run will set PORT; default to 8080
ENV PORT=8080

# Ensure Chrome binaries are discoverable
ENV GOOGLE_CHROME_SHIM=/usr/bin/google-chrome \
    CHROME_BIN=/usr/bin/google-chrome

EXPOSE 8080

# Start the FastAPI app with uvicorn, binding to Cloud Run's PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]