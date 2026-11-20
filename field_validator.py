"""from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
import email_validator
from typing import Annotated

class Patient(BaseModel):
    name :Annotated[str,Field(default="Biplav")]
    age : Annotated[int,Field(ge=18,le=60,title="Age constraints",description="the age should be 18 or greater than 18 and should be 60 or below 60")]
    email :EmailStr
    linkedin: AnyUrl

    @field_validator('email')
    @classmethod
    def email_valdia(cls,value):
        valid_domains=['gmail.com','srmist.edu']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('not a valid domain')
        return value
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print('database updated successfully')


patient_info={'name':'biplav','email':'pastrystrawberry99@gs.com','age':45,'linkedin':'https://wwww.google.com'}

patient_obj=Patient(**patient_info)
insert(patient_obj)
"""