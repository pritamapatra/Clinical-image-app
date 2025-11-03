import React from "react";
import { Table, TableHead, TableRow, TableCell, TableBody, Paper } from "@mui/material";

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
                {/* Use preview if you have a static file hosting backend, else skip for now */}
                {entry.filename}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}
