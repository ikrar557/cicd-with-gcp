from fastapi import FastAPI

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
def user_list()