#python
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List

#pydantic
from pydantic import BaseModel
from pydantic import Field,EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status

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

#Path parameters 


##Users
@app.post(
    path='/singnup',
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    summary='create_user',
    tags=['Users']
)
def signup():
    pass

@app.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary='Login_user',
    tags=['Users']
)
def Login():
    pass

@app.get(
    path='/users',
    status_code=status.HTTP_200_OK,
    response_model=List[User],
    summary='show_all_user',
    tags=['Users']
)
def Users():
    pass

@app.get(
    path='/users/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary='show_a_user',
    tags=['Users']
)
def user():
    pass

@app.delete(
    path='/users/{user_id}/delete',
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary='delete_user',
    tags=['Users']
)
def delete():
    pass

@app.put(
    path='/users/{user_id}/update',
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary='update_user',
    tags=['Users']
)
def update():
    pass


##Twitter
@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=List[twitter],
    summary='Home_twittes',
    tags=['Twitter']
    )
def home():
    return {'home': 'welcome to home'}

@app.post(
    path='/post',
    status_code=status.HTTP_201_CREATED,
    response_model=twitter,
    summary='post_twittes',
    tags=['Twitter']
    )
def post():
    pass

@app.get(
    path='/twittes/{twitte_id}',
    status_code=status.HTTP_200_OK,
    response_model=twitter,
    summary='show_a_twittes',
    tags=['Twitter']
    )
def twitte():
    pass

@app.delete(
    path='/twittes/{twitte_id}/delete',
    status_code=status.HTTP_200_OK,
    response_model=twitter,
    summary='delete_twitte',
    tags=['Twitter']
    )
def delete():
    pass

@app.put(
    path='/twittes/{twitte_id}/update',
    status_code=status.HTTP_200_OK,
    response_model=twitter,
    summary='update_twittes',
    tags=['Twitter']
    )
def update():
    pass