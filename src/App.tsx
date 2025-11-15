import { useState } from "react";
import { Header } from "./components/Header";
import { StatusIndicator } from "./components/StatusIndicator";
import { LatestPrediction } from "./components/LatestPrediction";
import { PredictionHistory } from "./components/PredictionHistory";
import { Sidebar } from "./components/Sidebar";
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner@2.0.3";

interface Prediction {
  id: string;
  weight: number;
  volume?: number;
  timestamp: Date;
  imageUrl?: string;
}

// Mock data for demonstration
const mockPredictions: Prediction[] = [
  {
    id: "5",
    weight: 18.45,
    volume: 22.3,
    timestamp: new Date(2025, 10, 12, 14, 23),
    imageUrl: "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=600"
  },
  {
    id: "4",
    weight: 15.72,
    volume: 19.1,
    timestamp: new Date(2025, 10, 12, 13, 15),
    imageUrl: "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=600"
  },
  {
    id: "3",
    weight: 21.38,
    volume: 25.8,
    timestamp: new Date(2025, 10, 12, 12, 45),
    imageUrl: "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=600"
  },
  {
    id: "2",
    weight: 17.91,
    volume: 21.6,
    timestamp: new Date(2025, 10, 12, 11, 30),
    imageUrl: "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=600"
  },
  {
    id: "1",
    weight: 19.25,
    volume: 23.2,
    timestamp: new Date(2025, 10, 12, 10, 12),
    imageUrl: "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=600"
  },
];

export default function App() {
  const [isConnected, setIsConnected] = useState(true);
  const [predictions, setPredictions] = useState<Prediction[]>(mockPredictions);
  const [latestPrediction, setLatestPrediction] = useState<Prediction | null>(
    mockPredictions[0] || null
  );

  const handleExportCSV = () => {
    // Create CSV content
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
    
    // Create and trigger download
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ffb-predictions-${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    toast.success("CSV exported successfully");
  };

  const handleClearHistory = () => {
    if (window.confirm("Are you sure you want to clear all prediction history?")) {
      setPredictions([]);
      setLatestPrediction(null);
      toast.success("History cleared");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-gray-600">Monitor and track FFB weight predictions in real-time</p>
          </div>
          <StatusIndicator isConnected={isConnected} />
        </div>

        <div className="grid lg:grid-cols-[1fr_320px] gap-6">
          <div className="space-y-6">
            <LatestPrediction prediction={latestPrediction} />
            
            <PredictionHistory
              predictions={predictions}
              onExportCSV={handleExportCSV}
              onClearHistory={handleClearHistory}
            />
          </div>

          <aside>
            <Sidebar />
          </aside>
        </div>
      </main>

      <Toaster />
    </div>
  );
}
