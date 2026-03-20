import { useEffect, useRef, useState } from "react";

// Components
import { Header } from "./components/Header";
import { CoverPage } from "./components/CoverPage";
import { MainNavigation } from "./components/MainNavigation";

// UI Components
import { Toaster } from "./components/ui/sonner";
import { toast } from "sonner";

// Types
import { Prediction } from "./types";

// API
import {
  getPredictions,
  checkBackendHealth,
  deleteAllPredictions,
  exportPredictionsCSV,
  getBagFiles,
} from "./services/api";
import type { BagFile } from "./services/api";

export default function App() {
  const [showCover, setShowCover] = useState(true);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [bagFiles, setBagFiles] = useState<BagFile[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const fadeOutTimerRef = useRef<ReturnType<typeof window.setTimeout> | null>(null);

  const latestPrediction = predictions[0] || null;

  useEffect(() => {
    const checkHealth = async () => {
      const healthy = await checkBackendHealth();
      setIsConnected(healthy);

      if (healthy) {
        loadPredictions();
        loadBagFiles();
      } else {
        setIsLoading(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

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
    } catch {
      toast.error("Failed to load predictions");
    } finally {
      setIsLoading(false);
    }
  };

  const loadBagFiles = async () => {
    try {
      const files = await getBagFiles();
      setBagFiles(files);
    } catch (error) {
      console.error(error);
    }
  };

  const handleUploadSuccess = () => {
    loadPredictions();
    loadBagFiles();
  };

  const handleExportCSV = async () => {
    try {
      await exportPredictionsCSV();
      toast.success("CSV exported");
    } catch {
      toast.error("Export failed");
    }
  };

  const handleClearHistory = async () => {
    if (window.confirm("Clear all history?")) {
      const success = await deleteAllPredictions();
      if (success) {
        setPredictions([]);
        toast.success("History cleared");
      }
    }
  };

  const handleEnterDashboard = () => {
    if (isFadingOut) return;
    setIsFadingOut(true);
    setShowDashboard(true);

    fadeOutTimerRef.current = window.setTimeout(() => {
      setShowCover(false);
    }, 600);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-rose-50 to-emerald-50 bg-fixed">
      
      {showCover && (
        <div className={`absolute inset-0 z-10 ${isFadingOut ? "animate-fade-out" : ""}`}>
          <CoverPage onEnter={handleEnterDashboard} disableIntroAnimation={isFadingOut} />
        </div>
      )}
  
      {showDashboard && (
        <div className="relative z-20 min-h-screen animate-fade-in">
          <Header />
  
          <MainNavigation
            isConnected={isConnected}
            latestPrediction={latestPrediction}
            predictions={predictions}
            bagFiles={bagFiles}
            onExportCSV={handleExportCSV}
            onClearHistory={handleClearHistory}
            onUploadSuccess={handleUploadSuccess}
          />
  
          <Toaster />
        </div>
      )}
  
    </div>
  );
}