import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Separator } from "./ui/separator";
import { HelpCircle, Settings, Info } from "lucide-react";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "./ui/accordion";

export function Sidebar() {
  return (
    <div className="space-y-4">

      {/* SETTINGS (ALWAYS VISIBLE AGAIN) */}
      <Card className="bg-white/80 backdrop-blur-md !border-2 !border-emerald-300 shadow-sm rounded-xl">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base text-emerald-800">
            <Settings className="w-4 h-4 text-emerald-700" />
            Settings
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <div>
            <label className="text-sm text-gray-600">Camera Resolution</label>
            <select className="w-full mt-1.5 px-3 py-2 bg-white border border-emerald-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-emerald-300">
              <option>1920 x 1080</option>
              <option>1280 x 720</option>
              <option>640 x 480</option>
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-600">Auto-save Predictions</label>
            <select className="w-full mt-1.5 px-3 py-2 bg-white border border-emerald-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-emerald-300">
              <option>Enabled</option>
              <option>Disabled</option>
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-600">History Limit</label>
            <select className="w-full mt-1.5 px-3 py-2 bg-white border border-emerald-200 rounded-lg text-sm focus:outline-none focus:ring-1 focus:ring-emerald-300">
              <option>50 records</option>
              <option>100 records</option>
              <option>200 records</option>
              <option>Unlimited</option>
            </select>
          </div>
        </CardContent>
      </Card>

      {/* HELP & INFO */}
      <Card className="bg-white/80 backdrop-blur-md !border-2 !border-emerald-300 shadow-sm rounded-xl">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-base text-emerald-800">
            <HelpCircle className="w-4 h-4 text-emerald-700" />
            Help & Info
          </CardTitle>
        </CardHeader>

        <CardContent>
          {/* Keep accordion INSIDE help (this was fine) */}
          <Accordion type="single" collapsible className="w-full">
            <AccordionItem value="item-1" className="border-emerald-200">
              <AccordionTrigger className="text-sm">How to use</AccordionTrigger>
              <AccordionContent className="text-sm text-gray-600">
                The dashboard automatically displays FFB weight predictions from the connected Odroid camera system.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-2" className="border-emerald-200">
              <AccordionTrigger className="text-sm">Exporting Data</AccordionTrigger>
              <AccordionContent className="text-sm text-gray-600">
                Click "Export CSV" to download prediction history for Excel or analysis tools.
              </AccordionContent>
            </AccordionItem>

            <AccordionItem value="item-3" className="border-emerald-200">
              <AccordionTrigger className="text-sm">Connection Status</AccordionTrigger>
              <AccordionContent className="text-sm text-gray-600">
                Green = connected, Red = disconnected. Check network if disconnected.
              </AccordionContent>
            </AccordionItem>
          </Accordion>

          <Separator className="my-4 bg-emerald-200" />

          <div className="space-y-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <Info className="w-4 h-4 text-emerald-700" />
              <span>Version 1.0.0</span>
            </div>
            <p className="text-xs">
              AI-powered FFB weight prediction system for precision agriculture.
            </p>
          </div>
        </CardContent>
      </Card>

    </div>
  );
}