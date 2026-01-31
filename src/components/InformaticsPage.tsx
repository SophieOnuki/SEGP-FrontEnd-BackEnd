import { Card } from "./ui/card";
import { Camera, Cpu, LineChart, Wifi, HardDrive, Zap } from "lucide-react";
import { ImageWithFallback } from "./ImageWithFallback";

export function InformaticsPage() {
  return (
    <main className="container mx-auto px-6 py-6">
      <div className="max-w-5xl mx-auto space-y-8">
        <div className="space-y-4">
          <h2>System Information</h2>
          <p className="text-gray-600">
            Learn about the FFB Weight Prediction System, its architecture, and how it works.
          </p>
        </div>

        <div className="rounded-lg overflow-hidden shadow-lg">
          <ImageWithFallback
            src="https://images.unsplash.com/photo-1639805855046-818d9159387b?w=1080"
            alt="Oil Palm Plantation"
            className="w-full h-64 object-cover"
          />
        </div>

        <Card className="p-6">
          <h3 className="mb-4">System Overview</h3>
          <p className="text-gray-700 mb-4">
            The FFB Weight Prediction System is an AI-powered solution designed for precision agriculture in oil palm plantations. 
            Using computer vision and machine learning, the system accurately estimates the weight of Fresh Fruit Bunches (FFB) 
            in real-time, helping optimize harvesting operations and improve yield predictions.
          </p>
          <p className="text-gray-700">
            Built on Odroid hardware, the system operates entirely offline, making it ideal for remote plantation locations 
            without reliable internet connectivity. All processing happens locally on the edge device, ensuring data privacy and 
            rapid response times.
          </p>
        </Card>

        <div>
          <h3 className="mb-6">Technical Architecture</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Camera className="w-6 h-6 text-blue-600" />
                </div>
                <h4>Image Capture</h4>
              </div>
              <p className="text-gray-700">
                High-resolution camera module captures FFB images. The system supports multiple camera configurations 
                and can process images in various lighting conditions.
              </p>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Cpu className="w-6 h-6 text-purple-600" />
                </div>
                <h4>AI Processing</h4>
              </div>
              <p className="text-gray-700">
                Deep learning models analyze FFB images to estimate weight and volume. The neural network was trained 
                on thousands of FFB samples for high accuracy.
              </p>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-green-100 rounded-lg">
                  <HardDrive className="w-6 h-6 text-green-600" />
                </div>
                <h4>Local Storage</h4>
              </div>
              <p className="text-gray-700">
                All predictions and images are stored locally on the Odroid. Data can be exported as CSV files 
                for further analysis and record-keeping.
              </p>
            </Card>

            <Card className="p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <Wifi className="w-6 h-6 text-orange-600" />
                </div>
                <h4>Real-Time Updates</h4>
              </div>
              <p className="text-gray-700">
                WebSocket communication enables instant updates to the dashboard. The connection status indicator 
                shows the current state of the Odroid link.
              </p>
            </Card>
          </div>
        </div>

        <Card className="p-6">
          <h3 className="mb-4">Hardware Specifications</h3>
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="mb-3">Odroid</h4>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>Quad-core ARM Cortex-A72 processor</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>4GB RAM for AI model inference</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>64GB microSD card for storage</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>Ethernet and WiFi connectivity</span>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="mb-3">Camera Module</h4>
              <ul className="space-y-2 text-gray-700">
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>Odroid Camera Module</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>8 megapixel resolution</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>Fixed focus lens optimized for FFB imaging</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-green-600 mt-1">•</span>
                  <span>Adjustable position mounting bracket</span>
                </li>
              </ul>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h3 className="mb-4">Model Performance</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center">
              <div className="flex justify-center mb-3">
                <div className="p-3 bg-green-100 rounded-full">
                  <LineChart className="w-8 h-8 text-green-600" />
                </div>
              </div>
              <h4 className="mb-2">±0.5 kg</h4>
              <p className="text-gray-600">Average Weight Accuracy</p>
            </div>
            <div className="text-center">
              <div className="flex justify-center mb-3">
                <div className="p-3 bg-blue-100 rounded-full">
                  <Zap className="w-8 h-8 text-blue-600" />
                </div>
              </div>
              <h4 className="mb-2">{"<"}2 sec</h4>
              <p className="text-gray-600">Inference Time</p>
            </div>
            <div className="text-center">
              <div className="flex justify-center mb-3">
                <div className="p-3 bg-purple-100 rounded-full">
                  <Cpu className="w-8 h-8 text-purple-600" />
                </div>
              </div>
              <h4 className="mb-2">93%</h4>
              <p className="text-gray-600">Model Accuracy</p>
            </div>
          </div>
        </Card>

        <div>
          <h3 className="mb-4">Use Cases & Benefits</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <Card className="p-4">
              <h4 className="mb-2">Harvest Optimization</h4>
              <p className="text-gray-700">
                Predict optimal harvest times by monitoring FFB weight progression over time, maximizing oil content.
              </p>
            </Card>
            <Card className="p-4">
              <h4 className="mb-2">Yield Forecasting</h4>
              <p className="text-gray-700">
                Accurate weight predictions enable better crop yield forecasting and production planning.
              </p>
            </Card>
            <Card className="p-4">
              <h4 className="mb-2">Quality Control</h4>
              <p className="text-gray-700">
                Consistent measurement standards ensure quality control across different harvesting teams.
              </p>
            </Card>
            <Card className="p-4">
              <h4 className="mb-2">Data Analytics</h4>
              <p className="text-gray-700">
                Export historical data for trend analysis, performance tracking, and decision-making insights.
              </p>
            </Card>
          </div>
        </div>

        <div className="text-center pt-8 border-t border-gray-200">
          <p className="text-gray-500">
            For technical support or questions about the system, please contact your system administrator.
          </p>
        </div>
      </div>
    </main>
  );
}