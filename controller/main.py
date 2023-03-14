from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn 
import os 
from dotenv import load_dotenv 
from controller.apis import Apis

app= FastAPI(title='Adidas-case-study', description='Training and Prediction APIs', version='1.0.0')
app.include_router(Apis)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def index():
	return "Hello, Welcome to the Model training and Prediction for Adidas Case Study"

if __name__ == "__main__":
	uvicorn.run("main:app", host='127.0.0.1', port=8001, reload=True)