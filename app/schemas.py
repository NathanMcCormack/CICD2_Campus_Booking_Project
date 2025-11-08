from typing import Annotated, Optional
from annotated_types import Ge, Le
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict 
 
NameStr = Annotated[str, StringConstraints(min_length=2, max_length=50)] 
StudentId = Annotated[str, StringConstraints(pattern=r"^G00\d{6}")] 
AgeInt = Annotated[int, Ge(16), Le(100)]
# PhoneStr = Annotated[str, StringConstraints(pattern=r"^\d{13}")] # all digits, 13 digits long 
PhoneStr = Annotated[str, StringConstraints(pattern=r'^\+353\s0\d{2}\s\d{3}\s\d{4}$')]
 
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

class UserUpdate(BaseModel): #Optional is for PATCH endpoints
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    student_id: Optional[str] = None