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
      <Card className="border-2 border-dashed">
        <CardContent className="flex items-center justify-center py-12">
          <p className="text-gray-500">No prediction available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-2 border-green-200 bg-green-50/50">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            Latest Prediction
            <Badge className="bg-green-600">Live</Badge>
          </CardTitle>
          <div className="flex items-center gap-1.5 text-sm text-gray-600">
            <Clock className="w-4 h-4" />
            {prediction.timestamp.toLocaleString()}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <div className="bg-white rounded-lg p-6 border border-green-200">
              <div className="flex items-start gap-3">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Weight className="w-6 h-6 text-green-700" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Predicted Weight</p>
                  <p className="text-green-900 mt-1">{prediction.weight.toFixed(2)} kg</p>
                </div>
              </div>
            </div>

            {prediction.volume !== undefined && (
              <div className="bg-white rounded-lg p-6 border border-green-200">
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <Box className="w-6 h-6 text-blue-700" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Volume</p>
                    <p className="text-blue-900 mt-1">{prediction.volume.toFixed(2)} L</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg p-4 border border-green-200">
            <p className="text-sm text-gray-600 mb-3">Captured Image</p>
            <div className="aspect-video bg-gray-100 rounded-lg overflow-hidden">
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
