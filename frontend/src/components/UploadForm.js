import React, { useState } from "react";
import { Button, TextField, Typography, Box, Paper } from "@mui/material";
import { useDropzone } from "react-dropzone";

export default function UploadForm({ onSubmit, fields, showDoctorNotes }) {
  const [form, setForm] = useState({});
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [notes, setNotes] = useState("");

  const onDrop = acceptedFiles => {
    const uploaded = acceptedFiles[0];
    setFile(uploaded);
    setPreview(URL.createObjectURL(uploaded));
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(form, file, notes);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  return (
    <Paper sx={{ p: 3 }}>
      <form onSubmit={handleSubmit}>
        {fields.map(field => (
          <TextField
            key={field}
            label={field}
            name={field}
            required
            fullWidth
            margin="normal"
            onChange={handleChange}
          />
        ))}
        {showDoctorNotes && (
          <TextField
            label="Doctor Notes"
            name="doctor_notes"
            multiline
            rows={2}
            fullWidth
            margin="normal"
            onChange={(e) => setNotes(e.target.value)}
          />
        )}
        <Box
          {...getRootProps()}
          border="2px dashed #1976d2"
          p={2}
          my={2}
          textAlign="center"
          sx={{ cursor: "pointer" }}
        >
          <input {...getInputProps()} />
          <Typography>
            {file ? `Selected: ${file.name}` : "Drag 'n' drop an image, or click to select"}
          </Typography>
          {preview && <img src={preview} alt="Preview" height={100} style={{ marginTop: 10 }} />}
        </Box>
        <Button variant="contained" color="primary" type="submit" fullWidth disabled={!file}>
          Upload
        </Button>
      </form>
    </Paper>
  );
}
