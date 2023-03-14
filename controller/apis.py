from fastapi import APIRouter, File, UploadFile, HTTPException, status, Response
import pandas as pd 
import logging.config
from services import serviceImpl
from pydantic_schemas import pydantic
from pydantic_schemas.response import Response as responseSchema 

Apis=APIRouter(prefix='/case_study/model', tags=['Apis'], responses=
	{404: responseSchema(code=404, status='Failure', message='Oops Invalid API !', result=[]).dict()},)

message="API executed Successfully"

@Apis.post('/training', status_code=status.HTTP_200_OK)
async def modeltrainingservice(file:UploadFile=File(...)):
	df=pd.read_csv(file.file)
	file.file.close()
	results = serviceImpl.model_training(df)
	return responseSchema(code=200, status='SUCCESS', message=message, result=results)

@Apis.post('/prediction', status_code=status.HTTP_200_OK)
async def modelpredictionservice(request: pydantic.Schema):
	results = serviceImpl.model_prediction(request)
	return responseSchema(code=200, status='SUCCESS', message=message, result=results)