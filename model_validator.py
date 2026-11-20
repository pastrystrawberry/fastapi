"""
from pydantic import (
    BaseModel, EmailStr, AnyUrl, Field,
    field_validator, model_validator
)
from typing import Annotated


class Patient(BaseModel):
    name: Annotated[str, Field(default="Biplav")]
    age: Annotated[
        int,
        Field(
            ge=18,
            le=60,
            title="Age constraints",
            description="Age must be between 18 and 60"
        )
    ]
    email: EmailStr
    linkedin: AnyUrl

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['gmail.com', 'srmist.edu']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not a valid email domain")

        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @model_validator(mode='after')
    def validate_patient(self):
        if self.age < 21 and self.name == "BIPLAV":
            raise ValueError(
                "Patients under 21 cannot use the default name Biplav"
            )

        return self


def insert(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print("Database updated successfully")


patient_info = {
    'name': 'biplav',
    'email': 'pastrystrawberry99@gmail.com',
    'age': 45,
    'linkedin': 'https://www.google.com'
}

patient_obj = Patient(**patient_info)
insert(patient_obj)
"""