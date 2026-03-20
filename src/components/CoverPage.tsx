import * as React from "react";
import { Button } from "./ui/button";
import { Brain, Activity, GlobeLock, TreePalm } from "lucide-react";

interface CoverPageProps {
  onEnter: () => void;
  disableIntroAnimation?: boolean;
}

export function CoverPage({ onEnter, disableIntroAnimation = false }: CoverPageProps) {
  return (
    <div
      className={`min-h-screen cover-page-animated-gradient flex flex-col items-center justify-center px-6 ${disableIntroAnimation ? "" : "animate-slide-up"}`}
    >
      <div className="max-w-4xl mx-auto text-center space-y-8">
        <div className="flex justify-center mb-4">
          <div className="relative">
            <div className="absolute inset-0 bg-green-400 blur-3xl opacity-20 rounded-full" />
            <div className="relative bg-white p-6 rounded-full shadow-lg">
              {/* Larger hero icon; matches the old hero dimensions */}
              <TreePalm className="text-green-600 w-16 h-16" />
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <h1 className="text-green-800">FFB Weight Prediction System</h1>
          <p className="text-gray-600 max-w-2xl mx-auto">
            AI-powered Fresh Fruit Bunch weight estimation for precision agriculture.
            Real-time predictions using computer vision and machine learning on Odroid.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 mt-12">
          <div className="bg-white p-6 rounded-lg shadow-md border border-green-100">
            <div className="flex justify-center mb-4">
              <Brain className="w-10 h-10 text-green-600" />
            </div>
            <h3 className="mb-2">AI Predictions</h3>
            <p className="text-gray-600">
              Advanced machine learning algorithms for accurate weight estimation
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-green-100">
            <div className="flex justify-center mb-4">
              <Activity className="w-10 h-10 text-green-600" />
            </div>
            <h3 className="mb-2">Real-Time Monitoring</h3>
            <p className="text-gray-600">
              Live updates and instant feedback on FFB measurements
            </p>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-green-100">
            <div className="flex justify-center mb-4">
              <GlobeLock className="w-10 h-10 text-green-600" />
            </div>
            <h3 className="mb-2">Offline Capable</h3>
            <p className="text-gray-600">
              Works locally on Odroid without internet connection
            </p>
          </div>
        </div>

        <div className="mt-12">
          <Button
            onClick={onEnter}
            size="lg"
            className="bg-green-600 hover:bg-green-700 px-8"
          >
            Enter Dashboard
          </Button>
        </div>

        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-gray-500">Odroid • Computer Vision • Machine Learning</p>
        </div>
      </div>
    </div>
  );
}
