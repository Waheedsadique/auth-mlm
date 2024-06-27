
from datetime import timedelta
from typing import Any
from passlib.context import CryptContext
from jose import jwt , JWTError


pwd_context = CryptContext(schemes=["bcrypt"])
secret_key = "baf8cdcf444543fa999dd27f1d138435ebb6f3bc610ed64518a8f43d6983"
algorithm = "HS256"



def generateToken(data: dict, expiry_time: timedelta):
   
    try:
        
        to_encode_data = data.copy()
        to_encode_data.update({
            "exp": expiry_time
        })
        
        token = jwt.encode(
            to_encode_data, secret_key, algorithm=algorithm)
        return token
    except JWTError as je:
        
        raise je
    


def passswordIntoHash(plaintext: str):
    
    
    hashedpassword = pwd_context.hash(plaintext)
    return hashedpassword


def verifyPassword(hashPass: str, plaintext: str):
    
   
    verify_password = pwd_context.verify(plaintext, hash=hashPass)
    return verify_password


def generateAccessAndRefreshToken(user_details: dict[str, Any]):
    
    print("User details in generate eccess an drefresh token funtion", user_details)
    # Constructing data payload for tokens
    data = {
        "user_name": user_details["user_name"],
        "user_email": user_details["user_email"],
        
    }
    # Generate access and refresh tokens
    access_token = generateToken(data, user_details["access_expiry_time"].total_seconds())
    refresh_token = generateToken(data, user_details["refresh_expiry_time"].total_seconds())
    access_expiry_time = user_details["access_expiry_time"]
    refresh_expiry_time = user_details["refresh_expiry_time"]

    return {
        "user_details": user_details,
        
        
        "access_token": {
            "token": access_token,
            "access_expiry_time": access_expiry_time
        },
        "refresh_token": {
            "token": refresh_token,
            "refresh_expiry_time": refresh_expiry_time
        }
    }