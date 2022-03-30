#python
from datetime import date, datetime
from uuid import UUID
from typing import Optional

#pydantic
from pydantic import BaseModel
from pydantic import Field,EmailStr

#FastAPI
from fastapi import FastAPI


class User_Base(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class User_Login(User_Base):
    password: str = Field(...,min_length=8,max_length=64)


class User(User_Base):
    first_name: str = Field(...,min_length=1,max_length=50)
    last_name: str = Field(...,min_length=1,max_length=50)
    birt_date: Optional[date] = Field(default=None)


class twitter(BaseModel):
    twitte_id: UUID = Field(...)
    contents: str = Field(...,min_length=1,max_length=264)
    create_at: datetime = Field(default=datetime.now())
    update_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

app = FastAPI()

@app.get('/')
def home():
    return {'home': 'welcome to home'}