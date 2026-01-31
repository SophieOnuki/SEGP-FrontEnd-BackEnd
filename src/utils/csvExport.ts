import { Prediction } from "../types";

export function exportPredictionsToCSV(predictions: Prediction[]): void {
  const headers = ["ID", "Weight (kg)", "Volume (L)", "Timestamp"];
  const rows = predictions.map(p => [
    p.id,
    p.weight.toFixed(2),
    p.volume?.toFixed(2) || "N/A",
    p.timestamp.toLocaleString()
  ]);
  
  const csvContent = [
    headers.join(","),
    ...rows.map(row => row.join(","))
  ].join("\n");
  
  const blob = new Blob([csvContent], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `ffb-predictions-${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

