from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import firestore

db = firestore.Client()

app = FastAPI()

students = [
    {'name': 'Student 1', 'age': 20},
    {'name': 'Student 2', 'age': 18},
    {'name': 'Student 3', 'age': 16}
]

class Student(BaseModel):
    name: str
    age: int

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/students")
def user_list():
    return {'students': students}

    
@app.get("/students/{student_id}")
def user_detail(student_id: str):
    doc_ref = db.collection('items').document(student_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        raise HTTPException(status_code= 404, detail="Student not found")

@app.post('/students')
async def user_add(student: Student):
    student_data = student.model_dump()
    doc_ref = db.collection('students').add(student_data)
    return {"id": doc_ref[1].id, "data":student_data}