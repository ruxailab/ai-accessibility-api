"""
ColorSense Routes - API endpoints for color contrast analysis
"""

from fastapi import APIRouter, HTTPException, Query, File, UploadFile, Form
from pydantic import BaseModel, HttpUrl
from typing import Optional
from ..controllers.colorsenseController import analyze_color_contrast_controller, analyze_html_contrast_controller

router = APIRouter()


class URLInput(BaseModel):
    url: HttpUrl
    add_tooltips: Optional[bool] = False


class HTMLInput(BaseModel):
    html: str
    add_tooltips: Optional[bool] = False


@router.post("/analyze-contrast/")
async def analyze_color_contrast(input_data: URLInput):
    """
    Analyze color contrast issues in a webpage
    
    - **url**: The URL of the webpage to analyze
    - **add_tooltips**: Whether to return HTML with visual markers for issues (default: False)
    
    Returns:
    - Analysis results with contrast issues found
    - Optionally includes marked HTML with tooltip indicators
    """
    url = str(input_data.url)
    add_tooltips = input_data.add_tooltips
    
    result = await analyze_color_contrast_controller(url, add_tooltips)
    
    if result is None:
        raise HTTPException(
            status_code=500, 
            detail=f"Could not fetch or process content from {url}"
        )
    
    return result


@router.post("/analyze-html/")
async def analyze_html_contrast(input_data: HTMLInput):
    """
    Analyze color contrast issues in HTML content provided by user
    
    - **html**: The HTML content to analyze
    - **add_tooltips**: Whether to return HTML with visual markers for issues (default: False)
    
    Returns:
    - Analysis results with contrast issues found
    - Optionally includes marked HTML with tooltip indicators
    
    Note: This endpoint is faster as it doesn't need to fetch content from a URL
    """
    html_content = input_data.html
    add_tooltips = input_data.add_tooltips
    
    result = await analyze_html_contrast_controller(html_content, add_tooltips)
    
    if result is None:
        raise HTTPException(
            status_code=500, 
            detail="Could not process the HTML content"
        )
    
    return result


@router.post("/analyze-html-file/")
async def analyze_html_file(
    file: UploadFile = File(...),
    add_tooltips: bool = Form(False)
):
    """
    Analyze color contrast issues in an HTML file upload
    
    - **file**: HTML file to analyze
    - **add_tooltips**: Whether to return HTML with visual markers for issues (default: False)
    
    Returns:
    - Analysis results with contrast issues found
    - Optionally includes marked HTML with tooltip indicators
    
    Note: This endpoint accepts file uploads, avoiding JSON escaping issues
    """
    try:
        # Read file content
        html_content = await file.read()
        html_str = html_content.decode('utf-8')
        
        result = await analyze_html_contrast_controller(html_str, add_tooltips)
        
        if result is None:
            raise HTTPException(
                status_code=500, 
                detail="Could not process the HTML file"
            )
        
        return result
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be a valid UTF-8 encoded HTML file"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )


@router.get("/health/")
async def health_check():
    """Health check endpoint for ColorSense service"""
    return {
        "service": "ColorSense",
        "status": "operational",
        "description": "Color contrast analyzer for WCAG compliance"
    }
