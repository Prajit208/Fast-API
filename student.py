from fastapi import FastAPI,Query, Path
from pydantic import BaseModel
from typing import Annotated
app=FastAPI()


class Students(BaseModel):
    
    name: str
    age: int
    grade: str

students = {
    1: {"name": "Prajit", "age": 21, "grade": "A"},
    2: {"name": "Ram", "age": 20, "grade": "B"},
    3: {"name": "Hari", "age": 22, "grade": "A"}
}

@app.get("/")
async def root():
    return{"message":"API is running"}

@app.get("/students")
async def students_display(name: str| None=None):
    if name:
        return{"Student": [s for s in students.values() if s==name]}
    return {"students": students}



@app.get("/students/{student_id}")
async def display_id(student_id: Annotated[int,Path(ge=1)]):
    if student_id in students:
        return {"student": students[student_id]}
    return {"error": "Student not found"}

@app.post("/students")
async def add_student(student: Students):
    new_id=max(students.keys())+1
    # update the existing dictionary
    students[new_id]={"name":student.name,
                        "age":student.age,
                        "grade":student.grade}
    return{
            "id":new_id,**students[new_id] # ** unpacks a python dictionary
        
    }

@app.put("/students/{student_id}") 
async def update_student(student_id: Annotated[int,Path(ge=1)],student: Students):
    if student_id in students:  
        students[student_id]={"name":student.name,
                        "age":student.age,
                        "grade":student.grade} 
        return{
            "id":student_id,**students[student_id]
        }
    return{"error":"Student not found"}        

@app.delete("/students/{student_id}")
async def delete_student(student_id: Annotated[int,Path(ge=1)]):
    if student_id in students:
        del students[student_id]
        return{"message":"Deleted"}
    return{"error":"Student not found"} 