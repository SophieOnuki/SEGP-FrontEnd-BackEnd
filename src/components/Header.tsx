import { FFBLogo } from "./FFBLogo";

export function Header() {
  return (
    <header className="border-b bg-white">
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-green-600 rounded-lg flex items-center justify-center">
            <FFBLogo className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-green-900">FFB Weight Prediction System</h1>
            <p className="text-sm text-gray-600">AI-Powered Fresh Fruit Bunch Analysis</p>
          </div>
        </div>
      </div>
    </header>
  );
}
