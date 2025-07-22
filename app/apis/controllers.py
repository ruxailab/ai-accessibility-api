from typing import List
from app.models.schema import Test

tests:List[Test]=[]


def getTest(testId):
    for i in tests:
        if i.testId==testId:
            return i

def addTest(newTest):
    tests.append(newTest)
    return tests
    