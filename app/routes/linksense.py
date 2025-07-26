from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from ..utils.fetcher import fetch_html_with_selenium
from ..controllers.anchorsenseController import analyse_anchor_tag


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