from fastapi import APIRouter, Response, status
from bson import ObjectId
from app.models.student import Student, StudentUpdate

from app.DB.mongoDB import MongoDB

router= APIRouter()


@router.post('/api/students')
async def create_student(student: Student, response: Response):
    studentId= await MongoDB.insert_student(student=student)
    response.status_code= status.HTTP_201_CREATED
    return {"id":studentId}

@router.get('/api/students')
async def get_student(country:str|None=None, age:str|None=None):
    students= await MongoDB.get_student(country, age)
    return students

@router.get("/api/students/{id}")
async def get_student_with_id(id):
    if not ObjectId.is_valid(id):
        return {}
    student= await MongoDB.get_student_with_id(id)
    return student

@router.patch('/api/students/{id}')
async def patch_student(id, student_update: StudentUpdate, response: Response):
    if not ObjectId.is_valid(id):
        return {}
    await MongoDB.update_student(id,student_update=student_update)
    response.status_code= status.HTTP_204_NO_CONTENT
    return {}

@router.delete('/api/students/{id}')
async def delete_student(id):
    if not ObjectId.is_valid(id):
        return {}
    await MongoDB.delete_student(id)
    return {}
    
    
