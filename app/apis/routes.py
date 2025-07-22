from fastapi import APIRouter
from app.models.schema import Test
from typing import List
from app.apis.controllers import getTest,addTest
router = APIRouter()




@router.get("/test/{testId}")
async def get_test_id(testId:str):
    data=getTest(testId)
    if data:
        return data
    else:
        return {"msg":"fail"}


@router.post("/test")
async def add_test(new_test:Test):
    newTest=addTest(new_test)
    return newTest



