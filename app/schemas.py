from typing import Annotated
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict 
 
NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)] 
StudentId = Annotated[str, StringConstraints(pattern=r"^G00\d{6}")] 
AgeInt = Annotated[int, Ge(16), Le(100)]
PhoneStr = Annotated[str, StringConstraints(pattern=r"^\d{13}")]
 
class UserCreate(BaseModel): 
    first_name: NameStr 
    last_name: NameStr #use the same annotation for names
    email: EmailStr
    phone: PhoneStr 
    age: AgeInt 
    student_id: StudentId 
 
class UserRead(BaseModel): 
    id: int 
    first_name: NameStr 
    last_name: NameStr 
    email: EmailStr
    phone: PhoneStr 
    age: AgeInt 
    student_id: StudentId 
 
    model_config = ConfigDict(from_attributes=True)