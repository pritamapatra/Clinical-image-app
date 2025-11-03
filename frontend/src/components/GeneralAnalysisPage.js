import React, { useState } from "react";
import UploadForm from "./UploadForm";
import { sendGeneralAnalysisUpload } from "../api/api";
import Dashboard from "./Dashboard";

const generalFields = ["name", "age", "gender", "doctor_id", "scan_date", "mri_sequence"];

export default function GeneralAnalysisPage() {
  const [entries, setEntries] = useState([]);

  // onSubmit handler for the form
  const handleUpload = async (form, file, doctorNotes) => {
    const data = new FormData();
    generalFields.forEach(f => data.append(f, form[f]));
    data.append("file", file);
    if (doctorNotes) data.append("doctor_notes", doctorNotes);

    try {
      const resp = await sendGeneralAnalysisUpload(data);
      setEntries([resp.data, ...entries].slice(0, 5)); // Show last 5
      alert("Uploaded and analyzed!");
    } catch (e) {
      alert("Upload error: " + (e?.response?.data?.detail || "Unknown error"));
    }
  };

  return (
    <>
      <UploadForm
        onSubmit={handleUpload}
        fields={generalFields}
        showDoctorNotes={true}
      />
      <Dashboard entries={entries} />
    </>
  );
}
