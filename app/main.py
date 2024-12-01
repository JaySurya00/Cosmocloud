from fastapi import FastAPI
from app.routers.students import router as student_router
from app.DB.mongoDB import MongoDB
import os

app= FastAPI()

@app.on_event("startup")
async def startup_event():
    if not os.getenv("MONGO_URI"):
        raise Exception("MONGO_URI not defined")
    await MongoDB.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await MongoDB.close()

app.include_router(student_router)