from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.schemas.patient import PatientInfo
from app.models.keras_model import brain_tumor_model
from app.utils.image_utils import detect_mime_type, extract_dicom_metadata, is_valid_medical_image
import pdfkit
from io import BytesIO
import base64
import os

# ---- Configurable paths and history settings ----
router = APIRouter()
BRAIN_TUMOR_HISTORY = {}
HISTORY_LIMIT = 5
UPLOAD_DIR = "uploaded_images"
WKHTMLTOPDF_PATH = r"C:\Users\ashut\OneDrive\wkhtmltopdf\bin\wkhtmltopdf.exe" # <--- Edit this if needed!

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---- Upload endpoint ----
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

    # Save image file (only for JPEG/PNG for PDF preview)
    file_type = detect_mime_type(contents)
    saved_path = None
    if file_type in ["image/jpeg", "image/png"]:
        saved_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(saved_path, "wb") as out_file:
            out_file.write(contents)

    # Validate file type
    if not is_valid_medical_image(contents):
        raise HTTPException(status_code=400, detail="Invalid file type. Only DICOM, JPEG, PNG allowed.")

    metadata = {}
    if file_type == "DICOM":
        metadata = extract_dicom_metadata(contents)
    else:
        metadata = {"info": f"{file_type} image detected"}

    prediction = brain_tumor_model.predict(contents)

    report = {
        "prediction": prediction,
        "patient": patient.dict(),
        "filename": file.filename,
        "file_type": file_type,
        "metadata": metadata,
        "saved_path": saved_path
    }

    # ---- Per-doctor history ----
    doctor_id_val = report["patient"]["doctor_id"]
    history = BRAIN_TUMOR_HISTORY.setdefault(doctor_id_val, [])
    history.append(report)
    if len(history) > HISTORY_LIMIT:
        history.pop(0)

    return report

# ---- History endpoint ----
@router.get("/history")
def get_brain_tumor_history(doctor_id: str = Query(...)):
    history = BRAIN_TUMOR_HISTORY.get(doctor_id, [])
    return {"doctor_id": doctor_id, "history": history}

# ---- PDF report endpoint ----
@router.get("/report/pdf")
def generate_pdf_report(doctor_id: str = Query(...), index: int = Query(0)):
    history = BRAIN_TUMOR_HISTORY.get(doctor_id, [])
    if not history or index >= len(history):
        raise HTTPException(status_code=404, detail="Report not found.")

    report = history[index]
    html = render_report_html(report)
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)

    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{doctor_id}_{index}.pdf"}
    )

# ---- HTML template helper ----
def render_report_html(report):
    patient = report["patient"]
    prediction = report["prediction"]
    filename = report["filename"]
    file_type = report["file_type"]
    metadata = report["metadata"]
    saved_path = report.get("saved_path", None)

    # Embed preview image
    img_html = ""
    if saved_path and file_type in ["image/jpeg", "image/png"] and os.path.isfile(saved_path):
        img_html = f'<img src="data:{file_type};base64,{image_to_base64(saved_path)}" width="256"/>'

    html = f"""
    <html>
    <head>
        <title>Brain Tumor Inference Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .section {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <h2>Brain Tumor Inference Report</h2>
        <div class="section">
            <strong>Patient Name:</strong> {patient['name']}<br>
            <strong>Age:</strong> {patient['age']}<br>
            <strong>Gender:</strong> {patient['gender']}<br>
            <strong>Doctor ID:</strong> {patient['doctor_id']}<br>
            <strong>Scan Date:</strong> {patient['scan_date']}<br>
            <strong>MRI Sequence:</strong> {patient['mri_sequence']}<br>
        </div>
        <hr>
        <div class="section">
            <strong>Prediction Result:</strong> {prediction['result']} ({round(float(prediction['confidence'])*100, 2)}%)<br>
            <strong>File Name:</strong> {filename}<br>
            <strong>File Type:</strong> {file_type}<br>
            <strong>Metadata:</strong> {metadata}<br>
        </div>
        <hr>
        {img_html}
    </body>
    </html>
    """
    return html

# ---- Image base64 helper ----
def image_to_base64(path):
    with open(path, "rb") as img_f:
        b64 = base64.b64encode(img_f.read()).decode("utf-8")
    return b64
