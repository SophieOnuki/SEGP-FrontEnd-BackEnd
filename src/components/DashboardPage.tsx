import { StatusIndicator } from "./StatusIndicator";
import { LatestPrediction } from "./LatestPrediction";
import { PredictionHistory } from "./PredictionHistory";
import { ImportedBagFiles } from "./ImportedBagFiles";
import { Sidebar } from "./Sidebar";
import { Prediction } from "../types";
import type { BagFile, UploadResponse } from "../services/api";

interface DashboardPageProps {
  isConnected: boolean;
  latestPrediction: Prediction | null;
  frameMasses?: number[];
  predictions: Prediction[];
  bagFiles: BagFile[];
  onExportCSV: () => void;
  onClearHistory: () => void;
  onUploadSuccess?: (result: UploadResponse) => void;
  onUploadStart?: () => void;
  onUploadError?: () => void;
}

export function DashboardPage({
  isConnected,
  latestPrediction,
  frameMasses,
  predictions,
  bagFiles,
  onExportCSV,
  onClearHistory,
  onUploadSuccess,
  onUploadStart,
  onUploadError,
}: DashboardPageProps) {
  return (
    <main className="container mx-auto px-6 py-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <p className="text-muted-foreground">
            Monitor and track FFB weight predictions in real-time
          </p>
        </div>
        <StatusIndicator isConnected={isConnected} />
      </div>

      <div className="grid lg:grid-cols-[1fr_320px] gap-6">
        <div className="space-y-6">

          <div className="bg-white/80 backdrop-blur-md rounded-xl border border-pink-100 shadow-sm hover:shadow-md transition">
            <LatestPrediction prediction={latestPrediction} frameMasses={frameMasses} />
          </div>

          <div className="bg-white/80 backdrop-blur-md rounded-xl border border-pink-100 shadow-sm hover:shadow-md transition">
            <ImportedBagFiles
              bagFiles={bagFiles}
              onUploadSuccess={onUploadSuccess}
              onUploadStart={onUploadStart}
              onUploadError={onUploadError}
            />
          </div>

          <div className="bg-white/80 backdrop-blur-md rounded-xl border border-pink-100 shadow-sm hover:shadow-md transition">
            <PredictionHistory
              predictions={predictions}
              onExportCSV={onExportCSV}
              onClearHistory={onClearHistory}
            />
          </div>

        </div>

        {/* Sidebar */}
        <aside className="bg-white/80 backdrop-blur-md rounded-xl border border-pink-100 shadow-sm p-4">
          <Sidebar />
        </aside>
      </div>
    </main>
  );
}
