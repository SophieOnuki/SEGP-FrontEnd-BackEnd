import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Download, Trash2, Weight, Clock } from "lucide-react";
import { ImageWithFallback } from "./ImageWithFallback";
import { Prediction } from "../types";
import { DEFAULT_FFB_IMAGE } from "../constants/images";

interface PredictionHistoryProps {
  predictions: Prediction[];
  onExportCSV: () => void;
  onClearHistory: () => void;
}

export function PredictionHistory({ predictions, onExportCSV, onClearHistory }: PredictionHistoryProps) {
  return (
    <Card className="border-emerald-200 bg-emerald-50">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Prediction History</CardTitle>
          <div className="flex gap-2">
            <Button
              onClick={onExportCSV}
              variant="outline"
              size="sm"
              className="gap-2 border-green-200/60 hover:border-green-200/70"
            >
              <Download className="w-4 h-4" />
              Export CSV
            </Button>
            <Button onClick={onClearHistory} variant="outline" size="sm" className="gap-2 text-destructive hover:text-destructive/90">
              <Trash2 className="w-4 h-4" />
              Clear History
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {predictions.length === 0 ? (
          <div className="text-center py-12 text-muted-foreground">
            No history available
          </div>
        ) : (
          <div className="space-y-3">
            {predictions.map((prediction) => (
              <div
                key={prediction.id}
                className="bg-emerald-50/60 rounded-lg p-4 border border-emerald-200 hover:border-emerald-200/70 hover:bg-emerald-100/60 hover-lift-sm transition-smooth"
              >
                <div className="flex gap-4">
                  <div className="w-24 h-24 bg-muted rounded-lg overflow-hidden flex-shrink-0">
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
                            <Weight className="w-4 h-4 text-secondary-foreground" />
                            <span className="text-secondary-foreground font-medium">{prediction.weight.toFixed(2)} kg</span>
                          </div>
                          {prediction.volume !== undefined && (
                            <span className="text-sm text-muted-foreground">
                              • {prediction.volume.toFixed(2)} L
                            </span>
                          )}
                        </div>
                        <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
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
