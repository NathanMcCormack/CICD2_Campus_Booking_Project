from pydantic import BaseModel, EmailStr, constr, conint

class User(BaseModel1):
    user_id: int
    name: constr(min_length=2, max_length=25)
    email: EmailStr # must follow correct email patterns 
    age: conint(gt=18) # age must be > 18
    student_id: constr(pattern=r'^G00\d{6}') # Student ID must start with "G00" followed by 6 digits 
