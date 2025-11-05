import React, { useEffect, useState } from "react";

function ReportHistory({ doctorId }) {
  const [reports, setReports] = useState([]);
  const backendUrl = "http://127.0.0.1:8000"; // Adjust if different

  useEffect(() => {
    // Fetch history for current doctor ID
    fetch(`${backendUrl}/history?doctor_id=${doctorId}`)
      .then((response) => response.json())
      .then((data) => setReports(data.history || []));
  }, [doctorId]);

  return (
    <div>
      <h2>Report History for Doctor: {doctorId}</h2>
      <table border="1">
        <thead>
          <tr>
            <th>Patient Name</th>
            <th>Scan Date</th>
            <th>Result</th>
            <th>Confidence</th>
            <th>Image Preview</th>
            <th>Heatmap</th>
            <th>Download PDF</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((report, idx) => (
            <tr key={idx}>
              <td>{report.patient.name}</td>
              <td>{report.patient.scan_date}</td>
              <td>{report.prediction.result}</td>
              <td>{(parseFloat(report.prediction.confidence) * 100).toFixed(2)}%</td>
              <td>
                {report.filename && (
                  <img
                    src={`${backendUrl}/images/${report.filename}`}
                    alt="Preview"
                    width="64"
                  />
                )}
              </td>
              <td>
                {report.heatmap_filename && (
                  <img
                    src={`${backendUrl}/images/${report.heatmap_filename}`}
                    alt="Heatmap"
                    width="64"
                  />
                )}
              </td>
              <td>
                <a
                  href={`${backendUrl}/report/pdf?doctor_id=${report.patient.doctor_id}&index=${idx}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Download PDF
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ReportHistory;
