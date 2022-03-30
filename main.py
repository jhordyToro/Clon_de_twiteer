#python
from datetime import date
from uuid import UUID
from typing import Optional

#pydantic
from pydantic import BaseModel
from pydantic import Field,EmailStr

#FastAPI
from fastapi import FastAPI

class user_base(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)
    
class user_login(user_base):
    password: str = Field(...,min_length=8)
    
class user(user_base):
    first_name: str = Field(...,min_length=1,max_length=50)
    last_name: str = Field(...,min_length=1,max_length=50)
    birt_date: Optional[date] = Field(default=None)

class twitter(BaseModel):
    pass

app = FastAPI()

@app.get('/')
def home():
    return {'home': 'welcome to home'}