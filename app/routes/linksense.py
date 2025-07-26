from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from utils.fetcher import fetch_html_with_selenium
from controllers.anchorsenseController import analyse_anchor_tag


router = APIRouter()

class URLInput(BaseModel):
    url: HttpUrl

@router.post("/analyze-links/")
async def analyze_links_route(input_data: URLInput):
    url = str(input_data.url)
    #fetch the html-content
    html_content=  fetch_html_with_selenium(url) 
    #feed the html-content to base-function
    result = await analyse_anchor_tag(html_content)
    
    if result is None:
        raise HTTPException(status_code=500, detail=f"Could not fetch or process content from {url}")
    
    return result