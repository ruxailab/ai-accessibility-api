from fastapi import APIRouter
from app.utils.fetcher import fetch_html_with_selenium

fetch_router=APIRouter()



@fetch_router.get("/fetch")
async def fetch_html_url(url:str):
    fetched_html=fetch_html_with_selenium(url)
    if fetched_html:
        return fetched_html
    else:
        return{"msg":"fail to fetch html"}
    
