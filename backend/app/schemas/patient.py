from pydantic import BaseModel

class PatientInfo(BaseModel):
    name: str
    age: int
    gender: str
    doctor_id: str
    scan_date: str
    mri_sequence: str
