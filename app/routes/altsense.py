from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, HttpUrl
from ..controllers.altsenseController import analyze_alt_attributes_controller, analyze_alt_attributes_from_html_controller

router = APIRouter()

class URLInput(BaseModel):
    url: HttpUrl

@router.post("/analyze-website-images/")
async def analyze_website_images_route(input_data: URLInput):
    url = str(input_data.url)
    
    result = await analyze_alt_attributes_controller(url)
    
    if result is None:
        raise HTTPException(status_code=500, detail=f"Could not fetch or process content from {url}")
    
    return result


@router.post("/analyze-file/")
async def analyze_html_file_route(file: UploadFile = File(...)):
    """
    Analyze alt attributes in an uploaded HTML file
    
    This endpoint:
    - Accepts HTML file upload
    - Analyzes all image tags for alt attribute issues
    - Returns list of accessibility issues found
    
    Upload:
        - file: HTML file (multipart/form-data)
    
    Returns:
        List of issues with details about missing or vague alt attributes
    """
    try:
        # Validate file type
        if not file.filename or not file.filename.endswith(('.html', '.htm')):
            raise HTTPException(
                status_code=400,
                detail="Only HTML files are supported (.html, .htm)"
            )
        
        # Read file content
        html_content = await file.read()
        html_string = html_content.decode('utf-8')
        
        # Analyze
        result = analyze_alt_attributes_from_html_controller(html_string)
        
        return result
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must be valid UTF-8 encoded HTML"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing HTML file: {str(e)}"
        )