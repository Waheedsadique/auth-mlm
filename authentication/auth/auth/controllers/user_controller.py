


from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlmodel import Session, select

from auth.controllers.auth_controllers import generateAccessAndRefreshToken, passswordIntoHash, verifyPassword
from auth.db.db import get_db
from auth.models.user_model import LoginModel, SignupModel, Token, User


access_expiry_time = timedelta(minutes=10)
refresh_expiry_time = timedelta(days=1)


DBSession = Annotated[Session, Depends(get_db)]


def signupFn(user_form: SignupModel, session: DBSession):

   
    users = session.exec(select(User))
    for user in users:
        is_email_exist = user.user_email == user_form.user_email
        is_password_exist = verifyPassword(
            user.user_password, user_form.user_password)

        if is_email_exist and is_password_exist:
            raise HTTPException(status_code=409, detail="email and password already exist")
        elif is_email_exist:
            raise HTTPException(status_code=409, detail="email already exist")
        elif is_password_exist:
            raise HTTPException(status_code=409, detail="password already exist")
    hashed_password = passswordIntoHash(user_form.user_password)


    user = User(user_name=user_form.user_name,
                user_email=user_form.user_email, user_password=hashed_password 
                , user_phone=user_form.user_phone, user_contry=user_form.user_contry
                , user_city=user_form.user_city, role=user_form.role, balance=user_form.balance, pin=user_form.pin)
    session.add(user)
    session.commit()
    session.refresh(user)

    data = {
        "user_name": user.user_name,
        "user_email": user.user_email,
        "user_phone": user.user_phone,
        "user_contry": user.user_contry,
        "user_city": user.user_city,
        "role": user.role,
        "balance": user.balance,
        "pin": user.pin,
        "access_expiry_time": access_expiry_time,
        "refresh_expiry_time": refresh_expiry_time
    }
    print(data)
    token_data = generateAccessAndRefreshToken(data)
    print({"token data " : token_data})

    # Save the refresh token in the database
    token = Token(user_id=user.user_id,
                  refresh_token=token_data["refresh_token"]["token"])
    session.add(token)
    session.commit()

    return token_data 



def loginFn(login_form: LoginModel, session: DBSession):
    
    print(login_form)
    users = session.exec(select(User))
    for user in users:
        user_email = user.user_email
        verify_password = verifyPassword(
            user.user_password, login_form.user_password)

        # Check if provided credentials are valid
        if user_email == login_form.user_email and verify_password:
            data = {
                "user_name": user.user_name,
                "user_email": user.user_email,
                "access_expiry_time": access_expiry_time,
                "refresh_expiry_time": refresh_expiry_time
            }
            token_data = generateAccessAndRefreshToken(data)

            # update the refresh token in the database
            token = session.exec(select(Token).where(
                Token.user_id == user.user_id)).one()
            token.refresh_token = token_data["refresh_token"]["token"]
            session.add(token)
            session.commit()
            session.refresh(token)
            return token_data
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
