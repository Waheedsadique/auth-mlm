from typing import Optional
from sqlmodel import SQLModel, Field

class LoginModel(SQLModel):
    user_email: str
    user_password: str  

class SignupModel(LoginModel):
    user_name: str
    user_phone: Optional[str]
    user_contry: Optional[str]
    user_city: Optional[str]
    role: Optional[str]
    balance: Optional[float]
    pin : Optional[str]
    
    

# Define User model
class User(SignupModel, table=True):
    user_id: Optional[int] = Field(None, primary_key=True)

# Define Token model
class Token(SQLModel, table=True):
    token_id: Optional[int] = Field(None, primary_key=True)
    user_id: int = Field(int, foreign_key="user.user_id")
    refresh_token: str