from fastapi import FastAPI
from .routes import altsense, linksense 

app = FastAPI(
    title="Web Accessibility Analyzer API",
    description="API for analyzing various accessibility aspects of websites, including alt text and link attributes.",
    version="1.0.0"
)

# Include routers from different modules
app.include_router(altsense.router, prefix="/altsense", tags=["AltSense Analysis"])
app.include_router(linksense.router, prefix="/linksense", tags=["LinkSense Analysis"]) 

@app.get("/")
async def root():
    return {"message": "Welcome to the Web Accessibility Analyzer API! Visit /docs for API documentation."}