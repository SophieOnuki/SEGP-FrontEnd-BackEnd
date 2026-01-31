import { Badge } from "./ui/badge";
import { Wifi, WifiOff } from "lucide-react";

interface StatusIndicatorProps {
  isConnected: boolean;
}

export function StatusIndicator({ isConnected }: StatusIndicatorProps) {
  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'} animate-pulse`} />
      <Badge variant={isConnected ? "default" : "destructive"} className="gap-1.5">
        {isConnected ? (
          <>
            <Wifi className="w-3 h-3" />
            Connected
          </>
        ) : (
          <>
            <WifiOff className="w-3 h-3" />
            Disconnected
          </>
        )}
      </Badge>
      <span className="text-sm text-gray-600">Odroid</span>
    </div>
  );
}
