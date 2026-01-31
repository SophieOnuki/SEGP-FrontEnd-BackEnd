import { useState } from "react";

// Components
import { Header } from "./components/Header";
import { CoverPage } from "./components/CoverPage";
import { MainNavigation } from "./components/MainNavigation";

// UI Components
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner@2.0.3";

// Types
import { Prediction } from "./types";

// Constants
import { mockPredictions } from "./constants/mockData";

// Utils
import { exportPredictionsToCSV } from "./utils/csvExport";

export default function App() {
  const [showCover, setShowCover] = useState(true);
  const [isConnected] = useState(true); // Would be updated via WebSocket in production
  const [predictions, setPredictions] = useState<Prediction[]>(mockPredictions);
  
  // Derive latest prediction from predictions array (always first item)
  const latestPrediction = predictions[0] || null;

  const handleExportCSV = () => {
    exportPredictionsToCSV(predictions);
    toast.success("CSV exported successfully");
  };

  const handleClearHistory = () => {
    if (window.confirm("Are you sure you want to clear all prediction history?")) {
      setPredictions([]);
      toast.success("History cleared");
    }
  };

  if (showCover) {
    return <CoverPage onEnter={() => setShowCover(false)} />;
  }

  return (
    <div className="min-h-screen bg-gray-50 animate-fade-in">
      <Header />
      
      <MainNavigation
        isConnected={isConnected}
        latestPrediction={latestPrediction}
        predictions={predictions}
        onExportCSV={handleExportCSV}
        onClearHistory={handleClearHistory}
      />

      <Toaster />
    </div>
  );
}