import { Card } from "./ui/card";
import { BookOpen, Eye, Download, Trash2, Wifi, Settings, BarChart3 } from "lucide-react";

export function UserManual() {
  return (
    <main className="container mx-auto px-6 py-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="space-y-4">
          <div className="flex items-center gap-3">
            <BookOpen className="w-8 h-8 text-green-600" />
            <h2 className="text-xl font-large">User Manual</h2>
          </div>
          <p className="text-muted-foreground">
            Learn how to use the FFB Weight Prediction System dashboard and make the most of its features.
          </p>
        </div>

        <Card className="p-6 border-emerald-200 bg-emerald-50">
          <h3 className="mb-4">Getting Started</h3>
          <p className="text-card-foreground mb-4">
            The FFB Weight Prediction System dashboard provides a real-time interface for monitoring and managing 
            Fresh Fruit Bunch (FFB) weight predictions from your Odroid camera system. This guide will help you 
            navigate the dashboard and understand all available features.
          </p>
          <p className="text-card-foreground">
            The dashboard consists of three main sections: <strong>Dashboard</strong> (main view), 
            <strong> System Information</strong> (technical details), and <strong>User Manual</strong> (this page).
          </p>
        </Card>

        <div>
          <h3 className="mb-6">Dashboard Features</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="p-6 hover-lift-sm border-emerald-200 bg-emerald-50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-secondary rounded-lg transition-smooth">
                  <Eye className="w-6 h-6 text-secondary-foreground" />
                </div>
                <h4>Latest Prediction</h4>
              </div>
              <p className="text-card-foreground mb-3">
                The top section displays the most recent FFB weight prediction with:
              </p>
              <ul className="space-y-2 text-card-foreground text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Predicted Weight:</strong> The estimated weight in kilograms</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Volume:</strong> Estimated volume in liters (when available)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Timestamp:</strong> When the prediction was made</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Captured Image:</strong> The FFB image used for prediction</span>
                </li>
              </ul>
            </Card>

            <Card className="p-6 hover-lift-sm border-emerald-200 bg-emerald-50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-accent rounded-lg transition-smooth">
                  <BarChart3 className="w-6 h-6 text-green-600" />
                </div>
                <h4>Prediction History</h4>
              </div>
              <p className="text-card-foreground mb-3">
                View all past predictions in chronological order. Each entry shows:
              </p>
              <ul className="space-y-2 text-card-foreground text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span>Thumbnail image of the FFB</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span>Weight and volume measurements</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span>Timestamp of the prediction</span>
                </li>
              </ul>
            </Card>

            <Card className="p-6 hover-lift-sm border-emerald-200 bg-emerald-50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-secondary rounded-lg transition-smooth">
                  <Download className="w-6 h-6 text-secondary-foreground" />
                </div>
                <h4>Export CSV</h4>
              </div>
              <p className="text-card-foreground mb-3">
                Export all prediction data to a CSV file for analysis:
              </p>
              <ol className="space-y-2 text-card-foreground text-sm list-decimal list-inside">
                <li>Click the "Export CSV" button in the Prediction History section</li>
                <li>The file will download automatically with today's date in the filename</li>
                <li>Open the CSV in Excel, Google Sheets, or any spreadsheet application</li>
                <li>The file contains: ID, Weight (kg), Volume (L), and Timestamp columns</li>
              </ol>
            </Card>

            <Card className="p-6 hover-lift-sm border-emerald-200 bg-emerald-50">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-destructive/10 rounded-lg transition-smooth">
                  <Trash2 className="w-6 h-6 text-destructive" />
                </div>
                <h4>Clear History</h4>
              </div>
              <p className="text-card-foreground mb-3">
                Remove all prediction history from the dashboard:
              </p>
              <ol className="space-y-2 text-card-foreground text-sm list-decimal list-inside">
                <li>Click the "Clear History" button in the Prediction History section</li>
                <li>Confirm the action in the popup dialog</li>
                <li>All predictions will be permanently removed</li>
                <li><strong>Note:</strong> Export your data first if you need to keep a record</li>
              </ol>
            </Card>
          </div>
        </div>

        <Card className="p-6 border-emerald-200 bg-emerald-50">
          <h3 className="mb-4">Understanding the Status Indicator</h3>
          <div className="flex items-start gap-4 mb-4">
            <div className="p-2 bg-secondary rounded-lg">
              <Wifi className="w-6 h-6 text-secondary-foreground" />
            </div>
            <div className="flex-1">
              <h4 className="mb-2">Connection Status</h4>
              <p className="text-card-foreground mb-3">
                The status indicator in the top-right corner shows the connection state to your Odroid device:
              </p>
              <ul className="space-y-2 text-card-foreground text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Green (Connected):</strong> The system is receiving predictions from the Odroid</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-destructive mt-1">•</span>
                  <span><strong>Red (Disconnected):</strong> No connection to the Odroid - check network settings</span>
                </li>
              </ul>
            </div>
          </div>
        </Card>

        <Card className="p-6 border-emerald-200 bg-emerald-50">
          <h3 className="mb-4">Sidebar Settings</h3>
          <div className="flex items-start gap-4 mb-4">
            <div className="p-2 bg-muted rounded-lg">
              <Settings className="w-6 h-6 text-muted-foreground" />
            </div>
            <div className="flex-1">
              <p className="text-card-foreground mb-3">
                The sidebar on the right side of the dashboard contains configuration options:
              </p>
              <ul className="space-y-2 text-card-foreground text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Camera Resolution:</strong> Adjust the capture resolution (1920x1080, 1280x720, or 640x480)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>Auto-save Predictions:</strong> Enable or disable automatic saving of predictions</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-secondary-foreground mt-1">•</span>
                  <span><strong>History Limit:</strong> Set maximum number of records to keep (50, 100, 200, or Unlimited)</span>
                </li>
              </ul>
            </div>
          </div>
        </Card>

        <div>
          <h3 className="mb-6">Tips & Best Practices</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="p-4 hover-lift-sm border-emerald-200 bg-emerald-50">
              <h4 className="mb-2">Regular Data Exports</h4>
              <p className="text-card-foreground text-sm">
                Export your prediction data regularly to maintain backups and enable long-term trend analysis.
              </p>
            </Card>
            <Card className="p-4 hover-lift-sm border-emerald-200 bg-emerald-50">
              <h4 className="mb-2">Monitor Connection Status</h4>
              <p className="text-card-foreground text-sm">
                Keep an eye on the connection indicator. If it shows disconnected, check your network connection and Odroid device status.
              </p>
            </Card>
            <Card className="p-4 hover-lift-sm border-emerald-200 bg-emerald-50">
              <h4 className="mb-2">Review Latest Predictions</h4>
              <p className="text-card-foreground text-sm">
                Check the Latest Prediction card frequently to see real-time updates from your Odroid camera system.
              </p>
            </Card>
            <Card className="p-4 hover-lift-sm border-emerald-200 bg-emerald-50">
              <h4 className="mb-2">Use History for Analysis</h4>
              <p className="text-card-foreground text-sm">
                The prediction history allows you to track trends over time and identify patterns in FFB weight measurements.
              </p>
            </Card>
          </div>
        </div>

        <Card className="p-6 bg-emerald-100/50 border border-emerald-200">
          <h3 className="mb-4">Need Help?</h3>
          <p className="text-card-foreground">
            If you encounter any issues or have questions about using the dashboard, please contact your system administrator 
            or refer to the System Information tab for technical details about the system architecture.
          </p>
        </Card>
      </div>
    </main>
  );
}

