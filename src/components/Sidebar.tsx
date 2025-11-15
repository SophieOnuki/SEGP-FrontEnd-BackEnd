import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";
import { HelpCircle, Settings, Info } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "./ui/accordion";

export function Sidebar() {
  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <Settings className="w-4 h-4" />
            Settings
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm text-gray-600">Camera Resolution</label>
            <select className="w-full mt-1.5 px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm">
              <option>1920 x 1080</option>
              <option>1280 x 720</option>
              <option>640 x 480</option>
            </select>
          </div>
          <div>
            <label className="text-sm text-gray-600">Auto-save Predictions</label>
            <select className="w-full mt-1.5 px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm">
              <option>Enabled</option>
              <option>Disabled</option>
            </select>
          </div>
          <div>
            <label className="text-sm text-gray-600">History Limit</label>
            <select className="w-full mt-1.5 px-3 py-2 bg-white border border-gray-300 rounded-lg text-sm">
              <option>50 records</option>
              <option>100 records</option>
              <option>200 records</option>
              <option>Unlimited</option>
            </select>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base">
            <HelpCircle className="w-4 h-4" />
            Help & Info
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="item-1">
              <AccordionTrigger className="text-sm">How to use</AccordionTrigger>
              <AccordionContent className="text-sm text-gray-600">
                The dashboard automatically displays FFB weight predictions from the connected Raspberry Pi camera system. Predictions appear in real-time with captured images.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-2">
              <AccordionTrigger className="text-sm">Exporting Data</AccordionTrigger>
              <AccordionContent className="text-sm text-gray-600">
                Click the "Export CSV" button to download all prediction history as a CSV file for further analysis in Excel or other tools.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-3">
              <AccordionTrigger className="text-sm">Connection Status</AccordionTrigger>
              <AccordionContent className="text-sm text-gray-600">
                The status indicator shows green when connected to the Raspberry Pi, and red when disconnected. Check your network connection if disconnected.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
          
          <Separator className="my-4" />
          
          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Info className="w-4 h-4" />
              <span>Version 1.0.0</span>
            </div>
            <p className="text-xs">AI-powered FFB weight prediction system for precision agriculture.</p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
