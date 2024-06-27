from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth.controllers.user_controller import loginFn, signupFn
from auth.db.db import create_db_and_tables


async def lifeSpan(app: FastAPI):
    
    print("Creating tables...")
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifeSpan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/signup")
async def signup(user_form: Annotated[dict, Depends(signupFn)]):
    if not user_form:
        raise HTTPException(status_code=400, detail="Bad request")
    return user_form


# make signin

@app.post("/api/signin")
async def signin(token_data: Annotated[dict, Depends(loginFn)]):
    if not token_data:
        raise HTTPException(status_code=400, detail="Bad request")
    #make return message you are login
    return token_data


# get all the user 


# @app.get("/api/users")
# async def get_users():