# A multi camera detection API  
from fastapi import FastAPI,File, UploadFile,status,Path,HTTPException
from typing import Annotated
from pydantic import BaseModel

app=FastAPI()

class Camera(BaseModel):
    name: str
    location: str
class Detection(BaseModel):
    camera_id:int
    filename: str
    file_size: int
    detected_action: str
    confidence: float

cameras={}
detections={}

@app.post("/cameras",status_code=status.HTTP_201_CREATED)
async def add_camera(new_camera : Camera):
    new_id= max(cameras.keys())+1 if cameras else 1
    cameras[new_id]={"name":new_camera.name,"location":new_camera.location}
    return{"details":cameras[new_id]}
    
@app.get("/cameras",status_code=status.HTTP_200_OK)
async def list_camera():
    return{"details":cameras}
    
@app.post("/cameras/{camera_id}/detect",status_code=status.HTTP_201_CREATED) 
async def detect(camera_id: Annotated[int,Path(ge=1)],file: UploadFile):
    if camera_id in cameras:
        contents=await file.read()
        new_id= max(detections.keys())+1 if detections else 1
        detections[new_id]={"camera_id":camera_id,"filename":file.filename,"file_size":len(contents),"detected_action":"punch","confidence":0.98}
        return {"detection": detections[new_id]}
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
    
            