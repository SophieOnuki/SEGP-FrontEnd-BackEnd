import { StatusIndicator } from "./StatusIndicator";
import { LatestPrediction } from "./LatestPrediction";
import { PredictionHistory } from "./PredictionHistory";
import { Sidebar } from "./Sidebar";
import { Prediction } from "../types";

interface DashboardPageProps {
  isConnected: boolean;
  latestPrediction: Prediction | null;
  predictions: Prediction[];
  onExportCSV: () => void;
  onClearHistory: () => void;
}

export function DashboardPage({
  isConnected,
  latestPrediction,
  predictions,
  onExportCSV,
  onClearHistory,
}: DashboardPageProps) {
  return (
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
            onExportCSV={onExportCSV}
            onClearHistory={onClearHistory}
          />
        </div>

        <aside>
          <Sidebar />
        </aside>
      </div>
    </main>
  );
}
