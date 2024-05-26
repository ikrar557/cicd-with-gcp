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
async def list_students():
    try:
        # Reference to the students collection
        students_ref = db.collection('students')
        # Fetch all documents in the students collection
        docs = students_ref.stream()

        # List to store student data
        students = []

        # Iterate over all documents and convert to dictionary
        for doc in docs:
            students.append(doc.to_dict())

        return {'students': students}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/students/{student_id}")
def user_detail(student_id: str):
    doc_ref = db.collection('students').document(student_id)
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