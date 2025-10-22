"""
New ColorSense Routes using Axe-Core
Clean, robust implementation for color contrast checking
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
from app.controllers.axe_contrast_controller import examine_url_contrast, examine_html_contrast


router = APIRouter(
    prefix="/colorsense",
    tags=["ColorSense - Axe-Core"]
)


class URLRequest(BaseModel):
    """Request model for URL-based contrast checking"""
    url: HttpUrl
    add_markers: Optional[bool] = True


@router.post("/examine")
async def examine_url(request: URLRequest):
    """
    Examine color contrast issues on a URL using axe-core
    
    This endpoint:
    - Takes a URL
    - Runs axe-core accessibility checks
    - Returns ONLY color-contrast violations
    - Optionally returns marked HTML with visual tooltips
    
    Returns:
        {
            "url": "...",
            "violations": [...],
            "total_issues": 0,
            "passed": true/false,
            "marked_html": "..." (if add_markers=true)
        }
    """
    try:
        result = await examine_url_contrast(
            url=str(request.url),
            add_markers=request.add_markers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing URL: {str(e)}")


@router.post("/examinehtml/")
async def examine_html_file(
    file: UploadFile = File(...),
    add_markers: bool = True
):
    """
    Examine color contrast issues in an HTML file using axe-core
    
    This endpoint:
    - Accepts HTML file upload
    - Runs axe-core accessibility checks
    - Returns ONLY color-contrast violations
    - Optionally returns marked HTML with visual tooltips
    
    Upload:
        - file: HTML file (multipart/form-data)
        - add_markers: boolean (optional, default=true)
    
    Returns:
        {
            "source": "html_content",
            "violations": [...],
            "total_issues": 0,
            "passed": true/false,
            "marked_html": "..." (if add_markers=true)
        }
    """
    try:
        # Validate file type
        if not file.filename.endswith('.html'):
            raise HTTPException(
                status_code=400,
                detail="Only HTML files are supported"
            )
        
        # Read file content
        html_content = await file.read()
        html_string = html_content.decode('utf-8')
        
        # Analyze
        result = await examine_html_contrast(
            html_content=html_string,
            add_markers=add_markers
        )
        
        # Add filename to result
        result['filename'] = file.filename
        
        return result
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be valid UTF-8 encoded HTML"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing HTML: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "ColorSense Axe-Core Integration",
        "version": "2.0",
        "engine": "axe-core"
    }
