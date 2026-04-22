from pydantic import BaseModel, Field



#join student pydantic model
class Student (BaseModel):
    name: str
    rollno : int = Field(gt=0)

    class Config :
        extra = "forbid"

class StudentJoinResponseModel (BaseModel):
    message:str
    data : Student

    class Config :
        extra = "forbid"

class student_mark (BaseModel):
    physics : float = Field(ge=0, le=100)
    chemistry : float = Field(ge=0, le=100)
    math : float = Field(ge=0, le=100)
    english : float = Field(ge=0, le=100)
    biology : float = Field(ge=0, le=100)
    IT : float = Field(ge=0, le=100)

    class Config :
        extra = "forbid"

class responsepercentage (BaseModel):
    name : str
    percentage : float
    grade : str

    class Config :
        extra = "forbid"


#signup pydantic model 
class SignupreqModel(BaseModel):
    username : str = Field(..., min_length=3)
    password : str = Field(..., min_length=6)

    class Config :
        extra = "forbid"

class SignupResponse(BaseModel):
    message : str

    class Config :
        extra = "forbid"


#login pydantic model
class LoginreqModel (BaseModel):
    username : str = Field(..., min_length=3)
    password : str = Field(..., min_length=6)

    class Config :
        extra = "forbid"

class LoginResponse (BaseModel):
    access_token : str
    token_type : str
    role : str

    class Config :
        extra = "forbid"

# create teacher pydantic model
class CreateTeacherReqModel (BaseModel):
    teacher_name : str = Field(..., min_length=5)

    class Config :
        extra = "forbid"

class CreateTeacherRespModel (BaseModel):
    message : str 
    username : str 

    class Config :
        extra = "forbid"


class markUpdateResponseModel(BaseModel):
    message : str

    class Config :
        extra = "forbid"






