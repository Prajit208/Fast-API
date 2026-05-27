from fastapi import FastAPI,File, UploadFile,status,Path,HTTPException
from typing import Annotated
from pydantic import BaseModel

app=FastAPI()

class Detection(BaseModel):
    filename: str
    file_size: float
    detection: str| None = None
    confidence: float| None= None
detections={}    
@app.post("/detect",status_code=status.HTTP_201_CREATED)
async def display_file(file: UploadFile):
    contents=await file.read()
    id=max(detections.keys())+1 if detections else 1
    detections[id]={"filename":file.filename,"filesize":len(contents),"detection":"A cat","confidence":0.96}
    return{"file_info":detections[id]}
@app.get("/detections")
 
async def all_detection():
    return {"Detections":detections} 
@app.get("/detections/{id}")

async def show_detection(id: Annotated[int,Path(ge=1)]):
    if id in detections:
        return{"file_info":detections[id]}
    raise HTTPException(status_code=404, detail="Detection not found")

@app.delete("/detections/{id}")
async def delete_detection(id: Annotated[int,Path(ge=1)]):
    if id in detections:
        del detections[id]
        return{"message":"Sucessfully deleted"}
    raise HTTPException(status_code=404, detail="Detection not found")