from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..controllers.geminisenseController import generate_gemini_suggestion

router = APIRouter()

class InputData(BaseModel):
    code: int
    module: str
    element: str
    issue: str
    help: str

@router.post("/suggestion/")
async def gemini_suggest(input_data: InputData):
    try:
        suggestion = await generate_gemini_suggestion(input_data)
        return {
            "input": input_data.dict(),
            "data": suggestion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
