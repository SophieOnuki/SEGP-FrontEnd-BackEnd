import * as Progress from "@radix-ui/react-progress";

interface ProgressBarProps {
  value: number;
  className?: string;
  showPercentage?: boolean;
}

export function ProgressBar({
  value,
  className = "",
  showPercentage = false
}: ProgressBarProps) {
  return (
    <div className={`w-full ${className}`}>
      <Progress.Root
        className="relative overflow-hidden bg-gray-200 rounded-full w-full h-2"
        value={value}
      >
        <Progress.Indicator
          className="bg-blue-600 w-full h-full transition-transform duration-300 ease-out"
          style={{ transform: `translateX(-${100 - value}%)`, backgroundColor: '#5C2A2E' }}
        />
      </Progress.Root>
      {showPercentage && (
        <p className="text-sm text-gray-600 mt-2 text-center">{value}%</p>
      )}
    </div>
  );
}
