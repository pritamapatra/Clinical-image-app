from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from schemas.patient import PatientInfo
from models.keras_model import brain_tumor_model
from utils.image_utils import detect_mime_type, extract_dicom_metadata, is_valid_medical_image


router = APIRouter()

@router.post("/upload")
async def upload_brain_tumor(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    doctor_id: str = Form(...),
    scan_date: str = Form(...),
    mri_sequence: str = Form(...),
    file: UploadFile = File(...)
):
    patient = PatientInfo(
        name=name,
        age=age,
        gender=gender,
        doctor_id=doctor_id,
        scan_date=scan_date,
        mri_sequence=mri_sequence
    )

    contents = await file.read()
    # Validate file type
    if not is_valid_medical_image(contents):
        raise HTTPException(status_code=400, detail="Invalid file type. Only DICOM, JPEG, PNG allowed.")

    file_type = detect_file_type(contents)
    metadata = {}
    if file_type == "DICOM":
        metadata = extract_dicom_metadata(contents)
    else:
        metadata = {"info": f"{file_type} image detected"}

    prediction = brain_tumor_model.predict(contents)

    return {
        "prediction": prediction,
        "patient": patient.dict(),
        "filename": file.filename,
        "file_type": file_type,
        "metadata": metadata
    }
