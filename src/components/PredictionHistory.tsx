import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Download, Trash2, Weight, Clock } from "lucide-react";
import { ImageWithFallback } from "./ImageWithFallback";
import { UploadBagButton } from "./UploadBagButton";
import { Prediction } from "../types";
import { DEFAULT_FFB_IMAGE } from "../constants/images";

interface PredictionHistoryProps {
  predictions: Prediction[];
  onExportCSV: () => void;
  onClearHistory: () => void;
  onUploadSuccess?: () => void;
}

export function PredictionHistory({ predictions, onExportCSV, onClearHistory, onUploadSuccess }: PredictionHistoryProps) {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Prediction History</CardTitle>
          <div className="flex gap-2">
            <UploadBagButton onUploadSuccess={onUploadSuccess} />
            <Button onClick={onExportCSV} variant="outline" size="sm" className="gap-2">
              <Download className="w-4 h-4" />
              Export CSV
            </Button>
            <Button onClick={onClearHistory} variant="outline" size="sm" className="gap-2 text-red-600 hover:text-red-700">
              <Trash2 className="w-4 h-4" />
              Clear History
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {predictions.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No history available
          </div>
        ) : (
          <div className="space-y-3">
            {predictions.map((prediction) => (
              <div
                key={prediction.id}
                className="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-green-300 hover:bg-green-50/30 transition-colors"
              >
                <div className="flex gap-4">
                  <div className="w-24 h-24 bg-gray-200 rounded-lg overflow-hidden flex-shrink-0">
                    <ImageWithFallback
                      src={prediction.imageUrl || DEFAULT_FFB_IMAGE}
                      alt="FFB"
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4">
                      <div className="space-y-2">
                        <div className="flex items-center gap-3">
                          <div className="flex items-center gap-1.5">
                            <Weight className="w-4 h-4 text-green-700" />
                            <span className="text-green-900">{prediction.weight.toFixed(2)} kg</span>
                          </div>
                          {prediction.volume !== undefined && (
                            <span className="text-sm text-gray-600">
                              • {prediction.volume.toFixed(2)} L
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-1.5 text-sm text-gray-600">
                          <Clock className="w-3.5 h-3.5" />
                          {prediction.timestamp.toLocaleString()}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
