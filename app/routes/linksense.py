from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, HttpUrl
from ..utils.fetcher import fetch_html_with_selenium
from ..controllers.anchorsenseController import analyse_anchor_tag, analyse_anchor_tag_from_html


router = APIRouter()

class URLInput(BaseModel):
    url: HttpUrl

@router.post("/analyze-links/")
async def analyze_links_route(input_data: URLInput):
    url = str(input_data.url)
    #fetch the html-content
   
    #feed the html-content to base-function
    result = await analyse_anchor_tag(url)
    
    if result is None:
        raise HTTPException(status_code=500, detail=f"Could not fetch or process content from {url}")
    
    return result


@router.post("/analyze-file/")
async def analyze_html_file_route(file: UploadFile = File(...)):
    """
    Analyze link accessibility in an uploaded HTML file
    
    This endpoint:
    - Accepts HTML file upload
    - Analyzes all anchor tags for accessibility issues
    - Returns list of issues found (non-descriptive links, missing href, etc.)
    
    Upload:
        - file: HTML file (multipart/form-data)
    
    Returns:
        List of issues with details about link accessibility problems
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
        result = analyse_anchor_tag_from_html(html_string)
        
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