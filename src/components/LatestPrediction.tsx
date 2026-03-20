import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Weight, Box, Clock } from "lucide-react";
import { ImageWithFallback } from "./ImageWithFallback";
import { Prediction } from "../types";
import { DEFAULT_FFB_IMAGE } from "../constants/images";

interface LatestPredictionProps {
  prediction: Prediction | null;
}

export function LatestPrediction({ prediction }: LatestPredictionProps) {
  if (!prediction) {
    return (
      <Card className="border-2 border-dashed border-emerald-200/80 bg-emerald-50 transition-smooth">
        <CardContent className="flex items-center justify-center py-12">
          <p className="text-muted-foreground">No prediction available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-2 border-emerald-200 bg-emerald-50 shadow-lg transition-smooth">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            Latest Prediction
            <Badge className="bg-secondary text-secondary-foreground shadow-sm transition-smooth">Live</Badge>
          </CardTitle>
          <div className="flex items-center gap-1.5 text-sm text-muted-foreground">
            <Clock className="w-4 h-4" />
            {prediction.timestamp.toLocaleString()}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-emerald-50 rounded-lg p-6 border border-emerald-200 shadow-sm hover:shadow-md transition-smooth">
              <div className="flex items-start gap-3">
                <div className="w-12 h-12 bg-gradient-to-br from-secondary to-secondary-foreground/20 rounded-lg flex items-center justify-center shadow-sm">
                  <Weight className="w-6 h-6 text-secondary-foreground" />
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Predicted Weight</p>
                  <p className="text-secondary-foreground font-semibold mt-1">{prediction.weight.toFixed(2)} kg</p>
                </div>
              </div>
            </div>

            {prediction.volume !== undefined && (
              <div className="bg-emerald-50 rounded-lg p-6 border border-emerald-200 shadow-sm hover:shadow-md transition-smooth">
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-accent to-secondary/50 rounded-lg flex items-center justify-center shadow-sm">
                    <Box className="w-6 h-6 text-accent-foreground" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Volume</p>
                    <p className="text-accent-foreground font-semibold mt-1">{prediction.volume.toFixed(2)} L</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200 shadow-sm hover:shadow-md transition-smooth">
            <p className="text-sm text-muted-foreground mb-3">Captured Image</p>
            <div className="aspect-video bg-emerald-50/60 rounded-lg overflow-hidden ring-1 ring-emerald-200/50">
              <ImageWithFallback
                src={prediction.imageUrl || DEFAULT_FFB_IMAGE}
                alt="FFB Capture"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
