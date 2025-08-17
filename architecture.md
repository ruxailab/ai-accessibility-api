# System Architecture Guide

## Overview

The Web Accessibility Analyzer API is built using **FastAPI** with a modular, service-oriented architecture. The system analyzes web pages for accessibility issues and provides AI-powered suggestions for improvements.

## Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client Apps   │────│   FastAPI API   │────│  Web Scraping   │
│                 │    │                  │    │   (Selenium)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                │
                       ┌────────▼────────┐
                       │  Analysis Core  │
                       │                 │
                       └────────┬────────┘
                                │
                       ┌────────▼────────┐
                       │   Gemini AI     │
                       │  Suggestions    │
                       └─────────────────┘
```

## Directory Structure

```
app/
├── main.py                 # FastAPI application entry point
├── routes/                 # API route definitions
│   ├── altsense.py        # Image alt text analysis routes
│   ├── linksense.py       # Link accessibility analysis routes
│   └── geminisense.py     # AI suggestion routes
├── controllers/           # Business logic controllers
│   ├── altsenseController.py
│   ├── anchorsenseController.py
│   └── geminisenseController.py
├── lib/                   # Core analysis libraries
│   ├── altsenelib.py      # Image alt text analysis logic
│   ├── anchorsense.py     # Link analysis logic
│   └── geminisuggester.py # AI suggestion integration
├── services/              # Additional service modules
├── utils/                 # Utility functions
│   ├── fetcher.py         # Web page fetching with Selenium
│   └── tagfetcher/        # HTML tag extraction utilities
├── models/                # Data models and schemas
└── docs/                  # Documentation files
```

## Core Components

### 1. API Layer (FastAPI)

**File**: `app/main.py`

- **Framework**: FastAPI with automatic OpenAPI documentation
- **Features**: 
  - Auto-generated interactive API docs at `/docs`
  - Input validation with Pydantic models
  - Async request handling
- **Endpoints**:
  - `/altsense/` - Image accessibility analysis
  - `/linksense/` - Link accessibility analysis  
  - `/geminisense/` - AI-powered suggestions

### 2. Routing Layer

**Files**: `app/routes/*.py`

- **Purpose**: Define API endpoints and request/response handling
- **Pattern**: Each route module focuses on specific accessibility domain
- **Validation**: Pydantic models for input validation (URL validation, data schemas)

### 3. Controller Layer

**Files**: `app/controllers/*.py`

- **Purpose**: Orchestrate business logic flow
- **Responsibilities**:
  - Coordinate between data fetching and analysis
  - Handle async operations
  - Error handling and logging
  - Return structured results

### 4. Analysis Libraries

**Files**: `app/lib/*.py`

#### AltSense Library (`altsenelib.py`)
- Analyzes `<img>` tags for accessibility issues
- Checks for missing alt attributes
- Validates alt text quality (non-vague descriptions)
- Returns structured issue reports

#### AnchorSense Library (`anchorsense.py`)
- Analyzes `<a>` tags for accessibility compliance
- Validates link text descriptiveness
- Checks external link handling
- Ensures keyboard accessibility
- Validates proper href usage

#### Gemini Suggester (`geminisuggester.py`)
- Integrates with Google's Gemini AI API
- Generates contextual improvement suggestions
- Provides expert accessibility recommendations

### 5. Web Scraping Layer

**File**: `app/utils/fetcher.py`

- **Technology**: Selenium WebDriver with Chrome
- **Features**:
  - Headless browser automation
  - JavaScript-rendered content support
  - Async wrapper for synchronous Selenium operations
  - Robust error handling

### 6. Tag Extraction Utilities

**File**: `app/utils/tagfetcher/tagFetcherUtil.py`

- **Purpose**: Extract specific HTML elements using BeautifulSoup
- **Functions**:
  - `get_img_tags_from_html()` - Extract image tags
  - `get_anchor_tags_from_html()` - Extract anchor tags
  - `get_aria_tags_from_html()` - Extract ARIA-related tags

## Data Flow

### 1. Image Analysis Flow

```
Client Request (URL) 
    ↓
Route Handler (/altsense/analyze-website-images/)
    ↓
Controller (analyze_alt_attributes_controller)
    ↓
Web Fetcher (fetch_html_with_selenium)
    ↓
Tag Extractor (get_img_tags_from_html)
    ↓
Analysis Library (analyze_image_tag)
    ↓
Response (Structured Issues List)
```

### 2. Link Analysis Flow

```
Client Request (URL)
    ↓
Route Handler (/linksense/analyze-links/)
    ↓
Controller (analyse_anchor_tag)
    ↓
Web Fetcher (fetch_html_with_selenium)
    ↓
Tag Extractor (get_anchor_tags_from_html)
    ↓
Analysis Library (analyze_anchor_tag)
    ↓
Response (Structured Issues List)
```

### 3. AI Suggestion Flow

```
Client Request (Issue Data)
    ↓
Route Handler (/geminisense/suggestion/)
    ↓
Controller (generate_gemini_suggestion)
    ↓
Gemini AI API (get_gemini_suggestion)
    ↓
Response (AI-Generated Suggestion)
```

## Technology Stack

### Backend Framework
- **FastAPI**: Modern, fast web framework for Python APIs
- **Uvicorn**: ASGI server for running FastAPI applications

### Web Scraping
- **Selenium WebDriver**: Browser automation for JavaScript-heavy sites
- **BeautifulSoup4**: HTML parsing and element extraction
- **Chrome/ChromeDriver**: Headless browser for content rendering

### AI Integration
- **Google Gemini AI**: Large language model for accessibility suggestions
- **google-generativeai**: Official Python SDK for Gemini API

### Data Validation
- **Pydantic**: Data validation and settings management
- **Type Hints**: Static type checking for better code quality

### Async Processing
- **AsyncIO**: Asynchronous programming support
- **Concurrent.futures**: Thread pool execution for Selenium operations

## Deployment Architecture

### Development
```
Developer Machine
├── Python Virtual Environment
├── Chrome Browser + ChromeDriver
├── FastAPI Development Server (uvicorn --reload)
└── Local Gemini AI API Access
```

### Production
```
Production Server
├── Docker Container (Optional)
│   ├── Python Runtime
│   ├── Chrome Browser (Headless)
│   └── Application Code
├── Load Balancer (Optional)
├── Reverse Proxy (Nginx/Apache)
└── Environment Variables (API Keys)
```

## Scalability Considerations

### Current Limitations
- **Single-threaded Selenium**: Each request uses one browser instance
- **Memory Usage**: Chrome instances consume significant memory
- **API Rate Limits**: Gemini AI API has usage quotas

### Scaling Strategies
1. **Horizontal Scaling**: Deploy multiple API instances behind load balancer
2. **Browser Pool**: Implement ChromeDriver connection pooling
3. **Caching**: Cache analysis results for frequently analyzed sites
4. **Queue System**: Implement async job queue for heavy analysis tasks
5. **Rate Limiting**: Add client rate limiting to prevent abuse

## Security Considerations

### Current Implementation
- Input validation for URLs using Pydantic
- Headless browser isolation
- No persistent data storage

### Recommended Enhancements
- **API Key Security**: Move to environment variables or secret management
- **Rate Limiting**: Implement per-client API rate limits  
- **Input Sanitization**: Additional URL validation and filtering
- **HTTPS Enforcement**: SSL/TLS for production deployments
- **CORS Configuration**: Proper cross-origin resource sharing setup

## Error Handling Strategy

### Error Types
1. **Network Errors**: Failed to fetch target website
2. **Parsing Errors**: Invalid HTML or missing elements
3. **API Errors**: Gemini AI service unavailable
4. **Validation Errors**: Invalid input parameters

### Error Response Format
```json
{
  "detail": "Error message description",
  "status_code": 500,
  "error_type": "specific_error_category"
}
```

## Future Architecture Enhancements

### Planned Improvements
1. **Database Layer**: Store analysis history and results
2. **Authentication**: User management and API key authentication
3. **Batch Processing**: Analyze multiple URLs in single request
4. **Real-time Monitoring**: Add logging and metrics collection
5. **Plugin Architecture**: Extensible analysis modules
6. **Webhook Support**: Notify clients when analysis completes

### Microservices Migration
Future consideration for breaking into microservices:
- **Analysis Service**: Core accessibility analysis
- **Scraping Service**: Web content fetching
- **AI Service**: Gemini AI integration
- **Gateway Service**: API routing and authentication
