from pydantic import BaseModel

class User_schema(BaseModel):
    username: str

class UserInform_schema(User_schema):
    password: str

class UserInDb_schema(UserInform_schema):
    id: int

    class Config:
        orm_mode = True


