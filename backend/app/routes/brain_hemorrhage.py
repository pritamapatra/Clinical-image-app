from fastapi import APIRouter, UploadFile, File, Form
from app.models.hemorrhage_model import predict

router = APIRouter()
BRAIN_HEMORRHAGE_HISTORY = {}

@router.post("/upload")
async def upload_brain_hemorrhage(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    doctor_id: str = Form(...),
    scan_date: str = Form(...),
    mri_sequence: str = Form(...),
    file: UploadFile = File(...)
):
    contents = await file.read()
    prediction = predict(contents)
    report = {
        "prediction": prediction,
        "patient": {
            "name": name,
            "age": age,
            "gender": gender,
            "doctor_id": doctor_id,
            "scan_date": scan_date,
            "mri_sequence": mri_sequence
        },
        "filename": file.filename
    }
    history = BRAIN_HEMORRHAGE_HISTORY.setdefault(doctor_id, [])
    history.append(report)
    if len(history) > 5:
        history.pop(0)
    return report

@router.get("/history")
def get_brain_hemorrhage_history(doctor_id: str):
    return {
        "doctor_id": doctor_id,
        "history": BRAIN_HEMORRHAGE_HISTORY.get(doctor_id, [])
    }
