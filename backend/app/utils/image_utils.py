import magic            # For MIME type detection (pip install python-magic)
import pydicom          # For DICOM metadata handling (pip install pydicom)
from io import BytesIO  # Utility for reading bytes into file-like objects

def detect_mime_type(file_bytes):
    """
    Detects the MIME type of input bytes.
    Returns a string like 'image/png', 'image/jpeg', or 'application/dicom'.
    """
    return magic.from_buffer(file_bytes, mime=True)

def extract_dicom_metadata(file_bytes):
    """
    Extracts key DICOM tags (PatientName, PatientID, etc) from a DICOM file.
    Returns a dictionary of metadata fields. If the file isn't DICOM or is corrupt, returns error info.
    """
    try:
        dicom_file = pydicom.dcmread(BytesIO(file_bytes))
        metadata = {
            "PatientName": str(getattr(dicom_file, "PatientName", "")),
            "PatientID": str(getattr(dicom_file, "PatientID", "")),
            "Modality": str(getattr(dicom_file, "Modality", "")),
            "StudyDate": str(getattr(dicom_file, "StudyDate", "")),
            "ScanType": str(getattr(dicom_file, "SeriesDescription", "")),
        }
        return metadata
    except Exception as e:
        return {"error": f"Failed to extract DICOM metadata: {str(e)}"}

def is_valid_medical_image(file_bytes):
    """
    Only returns True for acceptable medical formats: PNG, JPEG, DICOM.
    Uses MIME type detection for accuracy and security.
    """
    mime_type = detect_mime_type(file_bytes)
    return mime_type in ["image/png", "image/jpeg", "application/dicom"]
