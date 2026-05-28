# A multi camera detection API  
from fastapi import FastAPI,File, UploadFile,status,Path,HTTPException,BackgroundTasks
from typing import Annotated
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import time
app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Camera(BaseModel):
    name: str
    location: str
class Detection(BaseModel):
    camera_id:int
    filename: str
    file_size: int
    detected_action: str
    confidence: float 
    status: str| None=None

cameras={}
detections={}

def run_model_inference(detection_id: int,file_contents: bytes):
    time.sleep(3)# Simulate ML model processing time
    detections[detection_id].update({
        "detected_action": "punch",
        "confidence": 0.98,
        "status": "completed"
    })
    

@app.post("/cameras",status_code=status.HTTP_201_CREATED)
async def add_camera(new_camera : Camera):
    new_id= max(cameras.keys())+1 if cameras else 1
    cameras[new_id]={"name":new_camera.name,"location":new_camera.location}
    return{"details":cameras[new_id]}
    
@app.get("/cameras",status_code=status.HTTP_200_OK)
async def list_camera():
    return{"details":cameras}
    
@app.post("/cameras/{camera_id}/detect",status_code=status.HTTP_201_CREATED) 
async def detect(camera_id: Annotated[int,Path(ge=1)],file: UploadFile,background_tasks:BackgroundTasks):
    
    if camera_id in cameras:
        contents=await file.read()
        new_id= max(detections.keys())+1 if detections else 1
        
        # Create a placeholder record
        detections[new_id] = {
            "camera_id": camera_id,
            "filename": file.filename,
            "file_size": len(contents),
            "detected_action": "processing...",
            "confidence": 0.0,
            "status": "pending"
            }
        background_tasks.add_task(run_model_inference,new_id,contents)
        return{"message":"Inference started","detection id":new_id,"status":"pending"}
        
    else: raise HTTPException(status_code=404, detail="Camera ID not found")

@app.get("/cameras/{camera_id}/detections",status_code=status.HTTP_200_OK)
async def display_specific_camera(camera_id: Annotated[int,Path(ge=1)]):
    if camera_id not in cameras:
        raise HTTPException(status_code=404, detail="Camera not found")
    camera_detections={k:v for k,v in detections.items() if v["camera_id"]==camera_id}
    # Dictionarty caomprehenison, detection.items() give every key value pair, if condition check for exact camera id
    return{"detection":camera_detections}
    
@app.get("/cameras/{camera_id}/detections/{detection_id}",status_code=status.HTTP_200_OK)
async def display_specific_detection(camera_id: Annotated[int,Path(ge=1)],detection_id: Annotated[int,Path(ge=1)]):
    if camera_id not in cameras:
        raise HTTPException(status_code=404, detail="Camera not found")
    if detection_id not in detections:
        raise HTTPException(status_code=404, detail="Detection not found")
    if detections[detection_id]["camera_id"] != camera_id:
        raise HTTPException(status_code=404, detail="Detection not found for this camera")
    else:
        return{"detection":detections[detection_id]}
    
            