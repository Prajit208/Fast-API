from fastapi import FastAPI,Query

from typing import Annotated
app=FastAPI()

students = {
    1: "Prajit",
    2: "Ram",
    3: "Hari"
}
@app.get("/")
async def root():
    return{"message":"API is running"}

@app.get("/students")
async def students_display(name: str| None=None):
    if name:
        return{"Student": [s for s in students.values() if s==name]}
    return {"students": students}

# @app.get("/students/{student_id}")
# async def display_id(student_id : int,q: Annotated[str | None, Query(max_length=50)]= None ):
#     result={"Student ID":student_id}
#     if q:
#         result.update({"q": q})
#     return result    

@app.get("/students/{student_id}")
async def display_id(student_id: int):
    if student_id in students:
        return {"student": students[student_id]}
    return {"error": "Student not found"}

    