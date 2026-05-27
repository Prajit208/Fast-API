from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Path, Query
class Image(BaseModel):
    image_url: str

app = FastAPI()

@app.get("/")
async def root():
    return{"message":"api is running"}

@app.post("/predict")
async def predict(image: Image):
    return {
        "image_url":image.image_url,
        "prediction":"cat",
        "confidence":0.90
    }
    
    

