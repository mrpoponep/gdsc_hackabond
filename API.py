from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import create_quiz, auto_grading
import json

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
genai.configure(api_key='AIzaSyATnwbAxhJhdp1Kt075vK11QYwIGzjHB0E')


# Assuming create_quiz function is defined somewhere

app = FastAPI()

class QuizRequest(BaseModel):
    nums: int
    document: str
    instructions: str = ""

class QuizResponse(BaseModel):
    questions: str

@app.post("/generate_quiz/", response_model=QuizResponse)
async def generate_quiz(quiz_request: QuizRequest):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = create_quiz(model, quiz_request.nums, quiz_request.document, quiz_request.instructions)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Assuming auto_grading function is defined somewhere

class GradingRequest(BaseModel):
    json_data: dict

class GradingResponse(BaseModel):
    graded_data: dict

@app.post("/grade/", response_model=GradingResponse)
async def grade(json_request: GradingRequest):
    try:
        model = genai.GenerativeModel('gemini-pro')
        print(json_request)
        response_text = auto_grading(model, json_request.json_data)
        graded_data = json.loads(response_text)
        return GradingResponse(graded_data=graded_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)