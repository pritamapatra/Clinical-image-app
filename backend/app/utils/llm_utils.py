import requests

GEMINI_API_URL = "https://api.gemini.ai/v1/summarize"  # Example URL
GEMINI_API_KEY = "AIzaSyDV1ZjSHu5Jpq8bvrcE9GkUAXhIV1vH1V8"

def send_to_gemini_llm(image_bytes, doctor_notes):
    # Prepare the files and data for sending
    files = {
        "image": ("upload.png", image_bytes, "image/png"),  # Adjust name/type as needed
    }
    data = {
        "notes": doctor_notes,
        # May include other patient fields
    }
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}"
    }

    # Send request
    response = requests.post(GEMINI_API_URL, files=files, data=data, headers=headers)
    if response.status_code == 200:
        # Adjust based on actual Gemini response format
        payload = response.json()
        return {
            "summary": payload.get("summary", ""),
            "diagnosis": payload.get("diagnosis", ""),
            "recommendations": payload.get("recommendations", "")
        }
    else:
        return {
            "error": f"Gemini request failed: {response.status_code}",
            "details": response.text
        }
