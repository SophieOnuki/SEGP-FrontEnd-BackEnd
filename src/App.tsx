import { useEffect, useRef, useState } from "react";

// Components
import { Header } from "./components/Header";
import { CoverPage } from "./components/CoverPage";
import { MainNavigation } from "./components/MainNavigation";
import { ProgressBar } from "./components/ProgressBar";

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
  type UploadResponse,
} from "./services/api";
import type { BagFile } from "./services/api";
import {Spinner} from "./components/Spinner";

export default function App() {
  const [showCover, setShowCover] = useState(true);
  const [isFadingOut, setIsFadingOut] = useState(false);
  const [showDashboard, setShowDashboard] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [bagFiles, setBagFiles] = useState<BagFile[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  //--Progress state for uploads--
  const [isUploading, setIsUploading] = useState(false);
  const [uploadingProgress, setUploadingProgress] = useState(0);
  const uploadTimerRef = useRef<number | null>(null);

  const fadeOutTimerRef = useRef<number | null>(null);

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
        videoUrl: pred.videoUrl,
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

  //--Progress helpers--
  const startUploadProgress = () => {
    setIsUploading(true);
    setUploadingProgress(0);

    //Simulate progress till 90% while pipeline processes
    uploadTimerRef.current = window.setInterval(() => {
      setUploadingProgress((prev) => {
        if (prev >= 90) {
          window.clearInterval(uploadTimerRef.current!);
          return 90;
        }
        return prev + 5;
      });

    }, 1500);
  };

  const stopUploadProgress = (success: boolean) => {
    if (uploadTimerRef.current) {
      window.clearInterval(uploadTimerRef.current);
      uploadTimerRef.current = null;
    }

    if (success) {
      //Make 100% for user to see its complete
      setUploadingProgress(100);
      window.setTimeout(() => {
        setIsUploading(false);
        setUploadingProgress(0);
      }, 1100);
    } else {
      setIsUploading(false);
      setUploadingProgress(0);
    }
  };

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';


  const handleUploadSuccess = async (result: UploadResponse) => {
  const newPrediction: Prediction = {
    id: result.prediction.prediction_id.toString(),
    weight: result.prediction.mass_prediction,
    timestamp: new Date(result.prediction.created_at),
    videoUrl: result.video_url ? `${API_BASE_URL}${result.video_url}`
      : undefined,
  };
  setPredictions((prev) => [newPrediction, ...prev]);
  stopUploadProgress(true);
  await loadBagFiles(); // refresh bag files list
};

  const handleUploadStart = () => {
    startUploadProgress();
  };

  const handleUploadError = () => {
    stopUploadProgress(false);
    toast.error("Upload failed");
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

         {/* ── Upload progress overlay ─────────────────────────────── */}
          {isUploading && (
            <div className="fixed inset-x-0 top-0 z-50 flex flex-col items-center justify-center
                            bg-white/80 backdrop-blur-sm px-6 py-4 shadow-md">
              <div className="max-w-md w-full space-y-3">
                <div className="flex items-center gap-3">
                  <Spinner size={18} className="text-[#5C2A2E]" />
                  <p className="text-sm text-gray-700">
                    Uploading and processing bag file…
                  </p>
                </div>
                <ProgressBar value={uploadingProgress} showPercentage />
              </div>
            </div>
          )}
          {/* ────────────────────────────────────────────────────────── */}
  
          <MainNavigation
            isConnected={isConnected}
            latestPrediction={latestPrediction}
            predictions={predictions}
            bagFiles={bagFiles}
            onExportCSV={handleExportCSV}
            onClearHistory={handleClearHistory}
            onUploadSuccess={handleUploadSuccess}
            onUploadStart={handleUploadStart}
            onUploadError={handleUploadError}
          />
  
          <Toaster />
        </div>
      )}
  
    </div>
  );
}