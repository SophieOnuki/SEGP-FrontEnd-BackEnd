import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Weight, Box, Clock } from "lucide-react";
import { ImageWithFallback } from "./ImageWithFallback";
import { Prediction } from "../types";
import { DEFAULT_FFB_IMAGE } from "../constants/images";
import MassHistogram from "./MassHistogram";

const ODROID_STREAM_URL = "http://172.20.10.5:8080/";

interface LatestPredictionProps {
  prediction: Prediction | null;
  frameMasses?: number[];
}

function LiveCameraPanel() {
  const [streamError, setStreamError] = useState(false);
  const [streamKey, setStreamKey] = useState(0);

  return (
    <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200 shadow-sm hover:shadow-md transition-smooth">
      <div className="flex items-center justify-between mb-3">
        <p className="text-sm text-muted-foreground flex items-center gap-1.5">
          Live Camera Feed
          {!streamError && (
            <span className="flex items-center gap-1 text-xs text-emerald-600">
              <span className="inline-block w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              LIVE
            </span>
          )}
        </p>
        {streamError && (
          <button
            onClick={() => { setStreamError(false); setStreamKey((k) => k + 1); }}
            className="text-xs px-3 py-1 rounded-lg bg-emerald-100 text-emerald-700 hover:bg-emerald-200 transition"
          >
            Retry
          </button>
        )}
      </div>
      <div className="aspect-video bg-black rounded-lg overflow-hidden ring-1 ring-emerald-200/50">
        {streamError ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-400 gap-2">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                d="M15.75 10.5l4.72-4.72a.75.75 0 011.28.53v11.38a.75.75 0 01-1.28.53l-4.72-4.72M4.5 18.75h9a2.25 2.25 0 002.25-2.25v-9A2.25 2.25 0 0013.5 5.25h-9A2.25 2.25 0 002.25 7.5v9A2.25 2.25 0 004.5 18.75z" />
            </svg>
            <span className="text-sm">Stream unavailable</span>
            <span className="text-xs">{ODROID_STREAM_URL}</span>
          </div>
        ) : (
          <img
            key={streamKey}
            src={ODROID_STREAM_URL}
            alt="Live FFB camera feed"
            onError={() => setStreamError(true)}
            className="w-full h-full object-contain"
          />
        )}
      </div>
    </div>
  );
}

export function LatestPrediction({ prediction, frameMasses = [] }: LatestPredictionProps) {
  if (!prediction) {
    return (
      <Card className="border-2 border-dashed border-emerald-200/80 bg-emerald-50 transition-smooth">
        <CardContent className="pt-6 pb-4">
          <LiveCameraPanel />
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
          {/* Left: weight & volume */}
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

          {/* Right: processed video */}
          <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200 shadow-sm hover:shadow-md transition-smooth">
            <p className="text-sm text-muted-foreground mb-3">Processed Video</p>
            <div className="aspect-video bg-black rounded-lg overflow-hidden ring-1 ring-emerald-200/50">
              {prediction.videoUrl ? (
                <video
                  src={prediction.videoUrl}
                  controls={true}
                  autoPlay={true}
                  loop={true}
                  muted={true}
                  playsInline={true}
                  className="w-full h-full object-cover"
                />
              ) : (
                <ImageWithFallback
                  src={DEFAULT_FFB_IMAGE}
                  alt="No video available"
                  className="w-full h-full object-cover"
                />
              )}
            </div>
          </div>
        </div>

        {/* Live camera feed alongside the extracted video */}
        <div className="mt-6">
          <LiveCameraPanel />
        </div>

        {/* Histogram (only when frame masses exist) */}
        {frameMasses.length > 0 && (
          <div className="mt-8 pt-4 border-t border-emerald-200">
            <h3 className="text-md font-semibold text-emerald-800 mb-3">
              Mass distribution per frame
            </h3>
            <MassHistogram masses={frameMasses} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}