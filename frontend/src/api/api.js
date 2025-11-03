import axios from "axios";

export async function sendBrainTumorUpload(formData) {
  return axios.post("http://127.0.0.1:8000/api/brain-tumor/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}

export async function sendGeneralAnalysisUpload(formData) {
  return axios.post("http://127.0.0.1:8000/api/general-analysis/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });
}
