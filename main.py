"""
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pathlib import Path as FilePath
from typing import Annotated, Literal,Optional
from pydantic import BaseModel, Field, computed_field
import json

#app = FastAPI()


# Patient model
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient")]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., gt=0, description="Age of the patient")]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient")
    ]
    height: Annotated[
        float, Field(..., gt=0, description="Height in metres")
    ]
    weight: Annotated[
        float, Field(..., gt=0, description="Weight in kilograms")
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "overweight"
        else:
            return "obese"


# JSON file path
def get_file_path():
    return FilePath(__file__).parent / "patients.json"


# Load patient data
def load_data():
    file_path = get_file_path()

    with open(file_path, "r") as f:
        data = json.load(f)

    return data


# Save patient data
def save_data(data):
    file_path = get_file_path()

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# Home endpoint
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


# About endpoint
@app.get("/about")
def about():
    return {"message": "Functional API to manage records"}


# View all patients
@app.get("/view")
def view():
    return load_data()


# View a specific patient
@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(
        ...,
        description="ID of the patient in the database",
        example="P001"
    )
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


# Sort patients by height, weight, or BMI
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ...,
        description="Sort by height, weight, or bmi"
    ),
    order: str = Query(
        "asc",
        description="Sort order: asc or dsc"
    )
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Select from {valid_fields}"
        )

    if order not in ["asc", "dsc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Select asc or dsc"
        )

    data = load_data()

    def get_sort_value(patient_data):
        if sort_by == "bmi":
            return round(
                patient_data["weight"] / (patient_data["height"] ** 2),
                2
            )

        return patient_data.get(sort_by, 0)

    sorted_data = sorted(
        data.values(),
        key=get_sort_value,
        reverse=(order == "dsc")
    )

    return sorted_data


# Create a new patient
@app.post("/create", status_code=201)
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient data already exists"
        )

    # Convert the Pydantic model to a dictionary.
    # Exclude ID because it is already the dictionary key.
    patient_dict = patient.model_dump(exclude={"id"})

    data[patient.id] = patient_dict

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"message": "Patient created successfully"}
    )
class PatientUpdate(BaseModel):
    name:Annotated[Optional[str],Field(default=None)]
    city:Annotated[Optional[str],Field(default=None)]
    age :Annotated[Optional[int],Field(default=None)]
    gender:Annotated[Optional[Literal['male','female']],Field(default=None)]
    height:Annotated[Optional[float],Field(default=None, gt=0)]
    weight:Annotated[Optional[float],Field(default=None,gt=0)]
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient id not found")
    
    existing_info=data[patient_id]
    updated = patient_update.model_dump(exclude_unset=True)
    for key,value in updated.items():
        existing_info[key]=value
    existing_info['id']=patient_id
    pat_obj=Patient(**existing_info)
    data[patient_id] = pat_obj.model_dump(exclude={"id"})
    data[patient_id]=existing_info                    

    save_data(data)
    return JSONResponse(status_code=200, content={'message':'patient updated'})
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data= load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient id not found")
       
    del(data[patient_id])

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'message deleted'})
    """