"""from pydantic import BaseModel,EmailStr,AnyUrl,Field
import email_validator
from typing import Annotated

class Patient(BaseModel):
    name :Annotated[str,Field(default="Biplav")]
    age : Annotated[str,Field(ge=18,le=60,title="Age constraints",description="the age should be 18 or greater than 18 and should be 60 or below 60")]
    email :EmailStr
    linkedin: AnyUrl
def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print('database updated successfully')


patient_info={'name':'biplav','email':'pastrystrawberry99@gmail.com','age':61,'linkedin':'https://wwww.google.com'}

patient_obj=Patient(**patient_info)
insert(patient_obj)
"""