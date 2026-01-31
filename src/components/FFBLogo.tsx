interface FFBLogoProps {
  className?: string;
  size?: number;
}

// SVG representation of a Fresh Fruit Bunch (palm oil fruit cluster)
export function FFBLogo({ className = "", size = 24 }: FFBLogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Main stem */}
      <path
        d="M50 10 L50 90"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
      />
      {/* Fruit clusters - multiple bunches */}
      <circle cx="50" cy="25" r="8" fill="currentColor" opacity="0.9" />
      <circle cx="40" cy="30" r="7" fill="currentColor" opacity="0.85" />
      <circle cx="60" cy="30" r="7" fill="currentColor" opacity="0.85" />
      <circle cx="50" cy="40" r="9" fill="currentColor" opacity="0.9" />
      <circle cx="35" cy="45" r="6" fill="currentColor" opacity="0.8" />
      <circle cx="65" cy="45" r="6" fill="currentColor" opacity="0.8" />
      <circle cx="50" cy="55" r="10" fill="currentColor" opacity="0.95" />
      <circle cx="42" cy="60" r="7" fill="currentColor" opacity="0.85" />
      <circle cx="58" cy="60" r="7" fill="currentColor" opacity="0.85" />
      <circle cx="50" cy="70" r="8" fill="currentColor" opacity="0.9" />
      <circle cx="38" cy="75" r="6" fill="currentColor" opacity="0.8" />
      <circle cx="62" cy="75" r="6" fill="currentColor" opacity="0.8" />
    </svg>
  );
}

