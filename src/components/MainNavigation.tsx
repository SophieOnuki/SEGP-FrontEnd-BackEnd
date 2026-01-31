import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { DashboardPage } from "./DashboardPage";
import { InformaticsPage } from "./InformaticsPage";
import { UserManual } from "./UserManual";
import { Prediction } from "../types";

interface MainNavigationProps {
  isConnected: boolean;
  latestPrediction: Prediction | null;
  predictions: Prediction[];
  onExportCSV: () => void;
  onClearHistory: () => void;
}

export function MainNavigation({
  isConnected,
  latestPrediction,
  predictions,
  onExportCSV,
  onClearHistory,
}: MainNavigationProps) {
  return (
    <Tabs defaultValue="dashboard" className="w-full">
      <div className="border-b border-gray-200 bg-white">
        <div className="container mx-auto px-6">
          <TabsList className="bg-transparent h-12">
            <TabsTrigger value="dashboard" className="data-[state=active]:bg-gray-100">
              Dashboard
            </TabsTrigger>
            <TabsTrigger value="informatics" className="data-[state=active]:bg-gray-100">
              System Information
            </TabsTrigger>
            <TabsTrigger value="manual" className="data-[state=active]:bg-gray-100">
              User Manual
            </TabsTrigger>
          </TabsList>
        </div>
      </div>

      <TabsContent value="dashboard" className="mt-0 animate-fade-in">
        <DashboardPage
          isConnected={isConnected}
          latestPrediction={latestPrediction}
          predictions={predictions}
          onExportCSV={onExportCSV}
          onClearHistory={onClearHistory}
        />
      </TabsContent>

      <TabsContent value="informatics" className="mt-0 animate-fade-in">
        <InformaticsPage />
      </TabsContent>

      <TabsContent value="manual" className="mt-0 animate-fade-in">
        <UserManual />
      </TabsContent>
    </Tabs>
  );
}

