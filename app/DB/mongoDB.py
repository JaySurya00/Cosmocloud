from pymongo import AsyncMongoClient, ReturnDocument
from app.models.student import Student, StudentUpdate
from typing import Optional
from bson import ObjectId
import os

class MongoDBClient:
    __client: Optional[AsyncMongoClient] = None

    async def connect(self):
        if self.__client is not None:
            return self.__client
        try:
            self.__client = AsyncMongoClient(
                os.getenv("MONGO_URI")
            )
            DB= self.__client['Cosmocloud']
            self.students= DB["students"]
            server_info = await self.__client.server_info()
            print(f"Connected to MongoDB: {server_info}")
        except Exception as ex:
            raise Exception(f"Cannot connect to MongoDB: {ex}")
        
    async def close(self):
        try:
            await self.__client.close()
        except Exception as ex:
             raise Exception(f"Cannot disconnect to MongoDB: {ex}")
        
    async def insert_student(self, student: Student):
        try:
            if self.students is None:
                raise Exception("Cannot insert document before connection to MongoDB")
            student_dict= student.model_dump()
            studentId= (await self.students.insert_one(student_dict)).inserted_id
            return str(studentId)
        except Exception as ex:
            raise Exception(f"Error in MongoDB: {ex}")
        
    async def get_student(self, country: Optional[str]=None, age: Optional[int]=None):
        try:
            if self.students is None:
                raise Exception("Cannot insert document before connection to MongoDB")
            
            query={}
            if country:
                query["address.country"]=country
            if age:
                query["age"]= int(age)

            students=[]
            async for student in self.students.find(query):
                students.append({"name": student["name"], "age": student["age"]})
            return {"data": students}
        except Exception as ex:
            raise Exception(f"Error in MongoDB: {ex}")
        
    async def get_student_with_id(self, id:str):
        try:
            if self.students is None:
                raise Exception("Cannot insert document before connection to MongoDB")
            student= (await self.students.find_one({"_id": ObjectId(id)}))
            if not student:
                return {}
            return({"name": student["name"], "age": student["age"], "address": student["address"]})
        except Exception as ex:
            raise Exception(f"Error in MongoDB: {ex}")
        
    async def update_student(self, id:str, student_update: StudentUpdate):
        try:
            if self.students is None:
                raise Exception("Cannot insert document before connection to MongoDB")
            student_update_dict= student_update.model_dump(exclude_unset=True)
            student= await self.students.find_one({"_id": ObjectId(id)})
            
            if not student:
                return None
            
            if "address" in student_update_dict:
                address_update = student_update_dict.pop("address")
                merged_address = {**student.get("address", {}), **address_update}
                student_update_dict["address"] = merged_address
            
            updated_student = await self.students.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": student_update_dict},  # Update only the provided fields
                return_document=ReturnDocument.AFTER  # Return the updated document
            )
            return updated_student
        except Exception as ex:
            raise Exception(f"Error in MongoDB: {ex}")
        
    async def delete_student(self, id:str):
        try:
            if self.students is None:
                raise Exception("Cannot insert document before connection to MongoDB")
            student= (await self.students.find_one_and_delete({"_id": ObjectId(id)}))
        except Exception as ex:
            raise Exception(f"Error in MongoDB: {ex}")

MongoDB= MongoDBClient()