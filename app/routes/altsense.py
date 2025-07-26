from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from controllers.altsenseController import analyze_alt_attributes_controller

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