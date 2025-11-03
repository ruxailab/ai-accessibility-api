# Installation Guide

## Prerequisites

Before installing the Web Accessibility Analyzer API, ensure you have the following prerequisites:

- **Python 3.8+** (Recommended: Python 3.9 or higher)
- **Google Chrome Browser** (Required for Selenium WebDriver)
- **ChromeDriver** (Compatible with your Chrome version)
- **Gemini AI API Key** (For AI-powered accessibility suggestions)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/saltykheera/accessibility-api.git
cd accessibility-api
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. ChromeDriver Setup

#### Option A: Automatic Setup (Recommended)
The application uses Selenium with Chrome WebDriver. Ensure Google Chrome is installed on your system. ChromeDriver will be managed automatically by Selenium.

#### Option B: Manual Setup
1. Download ChromeDriver from [https://chromedriver.chromium.org/](https://chromedriver.chromium.org/)
2. Extract and place in your system PATH
3. Verify installation: `chromedriver --version`

### 5. Environment Configuration

#### Configure Gemini AI API Key

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Open `app/lib/geminisuggester.py`
3. Replace `"YOUR_GEMINI_API_KEY"` with your actual API key:

```python
genai.configure(api_key="your_actual_api_key_here")
```

**Security Note**: In production, use environment variables instead of hardcoding API keys.

### 6. Verify Installation

Run the test script to ensure everything is working:

```bash
python test.py
```

This should successfully fetch HTML content from a test website.

## Running the Application

### Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API Endpoint**: `http://localhost:8000`
- **Interactive Documentation**: `http://localhost:8000/docs`
- **Alternative Documentation**: `http://localhost:8000/redoc`

### Production Deployment

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Docker Installation (Optional)

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

# Install Chrome
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
docker build -t accessibility-api .
docker run -p 8000:8000 accessibility-api
```

## Troubleshooting

### Common Issues

1. **ChromeDriver Version Mismatch**
   - Ensure ChromeDriver version matches your Chrome browser version
   - Update Chrome browser and ChromeDriver

2. **Selenium WebDriver Issues**
   - Check if Chrome is installed and accessible
   - Verify ChromeDriver is in PATH
   - Try running in non-headless mode for debugging

3. **Permission Errors**
   - Ensure proper file permissions
   - Run with appropriate user privileges

4. **Network Issues**
   - Check internet connectivity for fetching web pages
   - Verify firewall settings don't block Chrome/ChromeDriver

5. **API Key Issues**
   - Verify Gemini AI API key is correct
   - Check API quota and billing status

### Getting Help

- Check the logs for detailed error messages
- Ensure all dependencies are correctly installed
- Verify Python version compatibility
- Review Chrome and ChromeDriver compatibility

## Next Steps

After successful installation:
1. Visit `/docs` endpoint for interactive API documentation
2. Test the API endpoints with sample URLs
