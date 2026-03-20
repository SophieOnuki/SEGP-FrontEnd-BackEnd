import { Badge } from "./ui/badge";
import { Wifi, WifiOff } from "lucide-react";

interface StatusIndicatorProps {
  isConnected: boolean;
}

export function StatusIndicator({ isConnected }: StatusIndicatorProps) {
  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full shadow-sm ${isConnected ? 'bg-secondary-foreground' : 'bg-destructive'} animate-pulse ring-2 ring-offset-2 ${isConnected ? 'ring-secondary-foreground/30' : 'ring-destructive/30'}`} />
      <Badge variant={isConnected ? "secondary" : "destructive"} className="gap-1.5">
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
      <span className="text-sm text-muted-foreground">Odroid</span>
    </div>
  );
}
