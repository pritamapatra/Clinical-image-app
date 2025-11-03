import React, { useState } from "react";
import UploadForm from "./UploadForm";
import { sendBrainTumorUpload } from "../api/api";
import Dashboard from "./Dashboard";

const brainFields = ["name", "age", "gender", "doctor_id", "scan_date", "mri_sequence"];

export default function BrainTumorPage() {
  const [entries, setEntries] = useState([]);

  const handleUpload = async (form, file) => {
    const data = new FormData();
    brainFields.forEach(f => data.append(f, form[f]));
    data.append("file", file);
    try {
      const resp = await sendBrainTumorUpload(data);
      setEntries([resp.data, ...entries].slice(0,5));
      alert("Uploaded and predicted!");
    } catch (e) {
      alert("Upload error: " + (e?.response?.data?.detail || "Unknown error"));
    }
  };

  return (
    <>
      <UploadForm onSubmit={handleUpload} fields={brainFields} />
      <Dashboard entries={entries} />
    </>
  );
}
