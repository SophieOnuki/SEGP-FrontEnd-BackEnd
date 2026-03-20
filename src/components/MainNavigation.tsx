import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { DashboardPage } from "./DashboardPage";
import { InformaticsPage } from "./InformaticsPage";
import { UserManual } from "./UserManual";
import { Prediction } from "../types";
import type { BagFile } from "../services/api";

interface MainNavigationProps {
  isConnected: boolean;
  latestPrediction: Prediction | null;
  predictions: Prediction[];
  bagFiles: BagFile[];
  onExportCSV: () => void;
  onClearHistory: () => void;
  onUploadSuccess?: () => void;
}

export function MainNavigation({
  isConnected,
  latestPrediction,
  predictions,
  bagFiles,
  onExportCSV,
  onClearHistory,
  onUploadSuccess,
}: MainNavigationProps) {
  return (
    <Tabs defaultValue="dashboard" className="w-full">
      <div className="border-b border-green-200/60 bg-emerald-50">
        <div className="container mx-auto px-6">
          <TabsList className="bg-transparent h-12 gap-1">
            <TabsTrigger
              value="dashboard"
              className="rounded-lg px-4 transition-all duration-300 text-green-800 data-[state=active]:bg-gradient-to-r data-[state=active]:from-accent data-[state=active]:to-secondary/80 data-[state=active]:text-accent-foreground data-[state=active]:font-medium data-[state=active]:shadow-sm hover:bg-accent/50"
            >
              Dashboard
            </TabsTrigger>
            <TabsTrigger
              value="informatics"
              className="rounded-lg px-4 transition-all duration-300 text-green-800 data-[state=active]:bg-gradient-to-r data-[state=active]:from-accent data-[state=active]:to-secondary/80 data-[state=active]:text-accent-foreground data-[state=active]:font-medium data-[state=active]:shadow-sm hover:bg-accent/50"
            >
              System Information
            </TabsTrigger>
            <TabsTrigger
              value="manual"
              className="rounded-lg px-4 transition-all duration-300 text-green-800 data-[state=active]:bg-gradient-to-r data-[state=active]:from-accent data-[state=active]:to-secondary/80 data-[state=active]:text-accent-foreground data-[state=active]:font-medium data-[state=active]:shadow-sm hover:bg-accent/50"
            >
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
          bagFiles={bagFiles}
          onExportCSV={onExportCSV}
          onClearHistory={onClearHistory}
          onUploadSuccess={onUploadSuccess}
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

