from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.patient import PatientInfo
from app.utils.image_utils import detect_mime_type, extract_dicom_metadata, is_valid_medical_image
import requests
import os

router = APIRouter()

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"
GEMINI_API_KEY = os.getenv("AIzaSyDV1ZjSHu5Jpq8bvrcE9GkUAXhIV1vH1V8") or "AIzaSyDV1ZjSHu5Jpq8bvrcE9GkUAXhIV1vH1V8"

@router.post("/upload")
async def upload_general_image(
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    doctor_id: str = Form(...),
    scan_date: str = Form(...),
    mri_sequence: str = Form(...),
    doctor_notes: str = Form(""),
    file: UploadFile = File(...)
):
    # 1. Collect patient info in a Pydantic model
    patient = PatientInfo(
        name=name,
        age=age,
        gender=gender,
        doctor_id=doctor_id,
        scan_date=scan_date,
        mri_sequence=mri_sequence
    )

    # 2. Load image bytes
    contents = await file.read()

    # 3. Validate that the file is a medical image
    if not is_valid_medical_image(contents):
        raise HTTPException(status_code=400, detail="Only PNG, JPEG, or DICOM images are accepted.")

    # 4. Detect MIME type
    mime_type = detect_mime_type(contents)

    # 5. Extract DICOM metadata if present
    dicom_metadata = {}
    if mime_type == "application/dicom":
        dicom_metadata = extract_dicom_metadata(contents)

    # 6. Encode image data as base64
    b64_image = base64.b64encode(contents).decode("utf-8")

    # 7. Prepare Gemini request JSON
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": doctor_notes or
                            "Please analyze this medical image and provide summary, diagnosis, recommendations."
                    },
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": b64_image
                        }
                    }
                ]
            }
        ]
    }

    # 8. Send request to Gemini API
    params = {"key": GEMINI_API_KEY}
    headers = {"Content-Type": "application/json"}
    gemini_response = requests.post(GEMINI_API_URL, params=params, headers=headers, json=body)

    if gemini_response.ok:
        payload = gemini_response.json()
        candidates = payload.get("candidates", [])
        gemini_text = ""
        if candidates:
            gemini_text = (
                candidates[0]
                .get("content", {})
                .get("parts", [{}])[0]
                .get("text", "")
            )
        # (Basic parsing -- you can add splitting logic for summary, diagnosis, recommendations!)
    else:
        gemini_text = f"GEMINI API ERROR ({gemini_response.status_code}): {gemini_response.text}"

    # 9. Return a structured response for your frontend
    return {
        "patient": patient.dict(),
        "filename": file.filename,
        "doctor_notes": doctor_notes,
        "mime_type": mime_type,
        "dicom_metadata": dicom_metadata,
        "gemini_report": gemini_text
    }
