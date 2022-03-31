#python
import json
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List

#pydantic
from pydantic import BaseModel
from pydantic import Field,EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body, HTTPException

class User_Base(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class User_Login(User_Base):
    password: str = Field(...,min_length=8,max_length=64)


class User(User_Base):
    first_name: str = Field(...,min_length=1,max_length=50)
    last_name: str = Field(...,min_length=1,max_length=50)
    birth_date: Optional[date] = Field(default=None)

class User_register(User):
    password: str = Field(...,min_length=8,max_length=64)

class tweet(BaseModel):
    tweet_id: UUID = Field(...)
    contents: str = Field(...,min_length=1,max_length=264)
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

app = FastAPI()


"""
# Auxiliar funcion 

## funcion reed
def read_data(file):
    with open("{}.json".format(file), "r+", encoding="utf-8") as f: 
        return json.loads(f.read())

## funcion write
def read_data(file, results):
    with open("{}.json".format(file), "r+", encoding="utf-8") as f: 
        f.seek(0)
        f.write(json.dumps(results))
"""


#Path parameters 


##Users
###Create a User
@app.post(
    path='/singnup',
    status_code=status.HTTP_201_CREATED,
    response_model=User,
    summary='create_user',
    tags=['Users']
)
def signup(user: User_register = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters: 
        - Request body parameter
            - user: User_Register
    
    Returns a json with the basic user information: 
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("Users.json","r+", encoding="utf-8") as f:
        results = json.loads(f.read())    ####leemos lo que esta dentro de la variable f y para que no nos muestre todo lo cargamos en formato json  
        user_dict = user.dict()           ####convertimos el valor que nos introduce el cliente y lo combertimos en dict
        user_dict["birth_date"] = str(user_dict["birth_date"])   ####comvertimos los valores birdate y userid manualmente a str para que no de error ya que la propia libreria no puede
        user_dict["user_id"] = str(user_dict["user_id"])
        results.append(user_dict) ### agregamos el usuario 
        f.seek(0)   ### esta linea de cocdigo es para poder mover al puntero de lectura al inicio y que no se salga ningun valor
        f.write(json.dumps(results)) ### escribimos el resultado directamente en el archivo f con el comando write y lo escribimos como json con el comando dumps
        return user

#········
###Login a user
@app.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    response_model=User_Base,
    summary='Login_user',
    tags=['Users']
)
def Login(email: EmailStr = Body(...), password: str = Body(...)):
    pass
    # with open('Users.json','r+',encoding='utf-8') as f:
    #     elements = json.loads(f.read())
    #     for element in elements:
    #         if element['password'] == password and element['email'] == email:
    #             return {'welcome to the twitter'}
    #         else:
    #             return {'status': 'false'}

###Show all users
@app.get(
    path='/users',
    status_code=status.HTTP_200_OK,
    response_model=List[User],
    summary='show_all_user',
    tags=['Users']
)
def Users():
    """
    This path operation shows all users in the app

    Parameters: 
        -

    Returns a json list with all users in the app, with the following keys: 
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open('Users.json','r',encoding='utf-8') as f:
        results = json.load(f)
        if len(results) == 0:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='Not content') 
        
        return results

#········
###Show a user
@app.get(
    path='/users/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary='show_a_user',
    tags=['Users']
)
def user():
    pass
    # return {'user': 'user if exist'}

###Delete a user
@app.delete(
    path='/users/{user_id}/delete',
    status_code=status.HTTP_200_OK,
    response_model=User,
    summary='delete_user',
    tags=['Users']
)
def delete():
    pass

###Update a user
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

###Show all tweets
@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=List[tweet],
    summary='Home_tweets',
    tags=['Twitter']
    )
def home():
    """
    Post show all Tweets

    This path operation post show all tweets in the app

    Parameters: 
        - Request body parameter
            - tweet: tweet
    
    Returns a json with all the tweets information: 
        tweet_id: UUID  
        content: str    
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    with open('tweets.json','r',encoding='utf-8') as f:
        tweets = json.load(f)
        return tweets

###Post a tweet
@app.post(
    path='/post',
    status_code=status.HTTP_201_CREATED,
    response_model=tweet,
    summary='post_a_tweet',
    tags=['Twitter']
    )
def post(tweet: tweet = Body(...)):
    """
    Post a Tweet
    This path operation post a tweet in the app
    Parameters: 
        - Request body parameter
            - tweet: Tweet
    
    Returns a json with the basic tweet information: 
        tweet_id: UUID  
        content: str    
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    with open('tweets.json','r+',encoding='utf-8') as f:
        result = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict['tweet_id'] = str(tweet_dict['tweet_id'])
        tweet_dict['created_at'] = str(tweet_dict['created_at'])
        tweet_dict['updated_at'] = str(tweet_dict['updated_at'])  
        tweet_dict['by']['user_id'] = str(tweet_dict['by']['user_id'])
        tweet_dict['by']['birth_date'] = str(tweet_dict['by']['birth_date'])

        result.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(result))
        return tweet

###show a tweeet
@app.get(
    path='/tweets/{tweet_id}',
    status_code=status.HTTP_200_OK,
    response_model=tweet,
    summary='show_a_tweets',
    tags=['Twitter']
    )
def twitte():
    pass

###Delete a Tweet
@app.delete(
    path='/tweets/{tweet_id}/delete',
    status_code=status.HTTP_200_OK,
    response_model=tweet,
    summary='delete_tweet',
    tags=['Twitter']
    )
def delete():
    pass

###Update a Tweet
@app.put(
    path='/tweets/{tweet_id}/update',
    status_code=status.HTTP_200_OK,
    response_model=tweet,
    summary='update_tweet',
    tags=['Twitter']
    )
def update():
    pass