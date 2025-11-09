import React from "react";
import { Table, TableHead, TableRow, TableCell, TableBody, Paper, Button } from "@mui/material";

const downloadPdfReport = async (doctorId, index) => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/brain-tumor/report/pdf?doctor_id=${doctorId}&index=${index}`,
      { method: "GET" }
    );
    if (!response.ok) throw new Error("Failed to download PDF");
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", `brain_tumor_report_${doctorId}_${index}.pdf`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  } catch (e) {
    alert("Error downloading PDF: " + e.message);
  }
};

export default function Dashboard({ entries }) {
  if (entries.length === 0) return null;

  return (
    <Paper sx={{ p: 2, mt: 4 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Patient Name</TableCell>
            <TableCell>Scan Date</TableCell>
            <TableCell>Result</TableCell>
            <TableCell>Confidence</TableCell>
            <TableCell>Preview</TableCell>
            <TableCell>Report</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {entries.map((entry, idx) => (
            <TableRow key={idx}>
              <TableCell>{entry.patient?.name}</TableCell>
              <TableCell>{entry.patient?.scan_date}</TableCell>
              <TableCell>{entry.prediction?.result}</TableCell>
              <TableCell>{entry.prediction?.confidence}</TableCell>
              <TableCell>
                {entry.filename}
              </TableCell>
              <TableCell>
                <Button
                  variant="contained"
                  color="primary"
                  size="small"
                  onClick={() => downloadPdfReport(entry.patient.doctor_id, idx)}
                >
                  Download PDF
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}
