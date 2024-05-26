from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {'name': 'Student 1', 'age': 20},
    {'name': 'Student 2', 'age': 18},
    {'name': 'Student 3', 'age': 16}
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/students")
def user_list():
    return {'students': students}

def student_check(student_id):
    if not students[student_id]:
        raise HTTPException(status_code=404, detail='Student not found')
    
@app.get("/students/{student_id}")
def user_detail(student_id: int):
    student_check(student_id)
    return {'student' : students[student_id]}

@app.post('/students')
def user_add(student: Student):
    student.append(student)
    
    return {'student': student[-1]}