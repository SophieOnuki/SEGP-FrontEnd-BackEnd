import { useState, useEffect } from "react";

// Components
import { Header } from "./components/Header";
import { CoverPage } from "./components/CoverPage";
import { MainNavigation } from "./components/MainNavigation";

// UI Components
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner";

// Types
import { Prediction } from "./types";

// API Calling
import {
  getPredictions,
  getLatestPrediction,
  checkBackendHealth,
  deleteAllPredictions,
  deletePrediction,
  exportPredictionsCSV
} from "./services/api";

// // Constants
// import { mockPredictions } from "./constants/mockData";

// Utils
import { exportPredictionsToCSV } from "./utils/csvExport";

export default function App() {
  const [showCover, setShowCover] = useState(true);
  const [isConnected, setIsConnected] = useState(false); // Would be updated via WebSocket in production
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Derive latest prediction from predictions array (always first item)
  const latestPrediction = predictions[0] || null;

  //Check backend health on mount and periodically
  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await checkBackendHealth();
      setIsConnected(healthy);


      if (healthy) {
        loadPredictions();
      } else {
        setIsLoading(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  // Function to load predictions from backend
  const loadPredictions = async () => {
    try {
      setIsLoading(true);
      const data = await getPredictions();

      const convertedData = data.map((pred) => ({
        id: pred.prediction_id.toString(),
        weight: pred.mass_prediction,
        timestamp: new Date(pred.created_at),
      }));

      setPredictions(convertedData);
    } catch (error) {
      toast.error("Failed to load predictions from backend");
    } finally {
      setIsLoading(false);
    }
  };


  const handleExportCSV = async () => {
    try {
      await exportPredictionsCSV();
      toast.success("CSV exported successfully");
    } catch (error) {
      console.error("Error exporting CSV:", error);
      toast.error("Failed to export CSV");
    }
  };


  const handleClearHistory = async () => {
    if (window.confirm("Are you sure you want to clear all prediction history?")) {
      try {
        const success = await deleteAllPredictions();
        if (success) {
          setPredictions([]);
          toast.success("History cleared");
        } else {
          toast.error("Failed to clear history");
        }
      } catch (error) {
        console.error("Error clearing history:", error);
        toast.error("Failed to clear history");
      }
    }
  };

  if (showCover) {
    return <CoverPage onEnter={() => setShowCover(false)}/>;
  }

  return (
      <div className="min-h-screen bg-gray-50 animate-fade-in">
        <Header/>

        <MainNavigation
            isConnected={isConnected}
            latestPrediction={latestPrediction}
            predictions={predictions}
            onExportCSV={handleExportCSV}
            onClearHistory={handleClearHistory}
            onUploadSuccess={loadPredictions}
        />

        <Toaster/>
      </div>
  );
}
