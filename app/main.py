from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import altsense, linksense, geminisense, colorsense, axe_colorsense

app = FastAPI(
    title="Web Accessibility Analyzer API",
    description="API for analyzing various accessibility aspects of websites, including alt text, link attributes, and color contrast.",
    version="2.0.0"
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include routers from different modules
app.include_router(altsense.router, prefix="/altsense", tags=["AltSense Analysis"])
app.include_router(linksense.router, prefix="/linksense", tags=["LinkSense Analysis"]) 
app.include_router(geminisense.router, prefix="/geminisense", tags=["GeminiSense Analysis"])
# app.include_router(colorsense.router, prefix="/colorsense-old", tags=["ColorSense Analysis - Deprecated"])  # Old implementation
app.include_router(axe_colorsense.router, tags=["ColorSense Analysis"]) 

@app.get("/")
async def root():
    return {"message": "Welcome to the Web Accessibility Analyzer API! Visit /docs for API documentation."}