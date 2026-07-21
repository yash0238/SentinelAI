"use client";

/**
 * RiskGauge — Animated circular risk-score gauge.
 *
 * Props:
 *   score    — 0–100
 *   risk     — "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
 *   size     — diameter in px (default 120)
 *   label    — optional text below the gauge
 */

import { RISK_COLORS } from "@/lib/mock-data";

export default function RiskGauge({
  score = 0,
  risk = "LOW",
  size = 120,
  label,
}) {
  const color = RISK_COLORS[risk] || "#4da6ff";
  const radius = (size - 12) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
  const center = size / 2;

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg width={size} height={size} className="-rotate-90">
          {/* Background track */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="#1a2236"
            strokeWidth={6}
          />
          {/* Progress arc */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke={color}
            strokeWidth={6}
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={circumference - progress}
            style={{
              transition: "stroke-dashoffset 1s ease-out",
              filter: `drop-shadow(0 0 6px ${color}66)`,
            }}
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span
            className="text-xl font-extrabold"
            style={{ color }}
          >
            {score}
          </span>
          <span className="text-[0.6rem] text-slate-500 font-medium">/100</span>
        </div>
      </div>
      {label && (
        <span className="text-[0.75rem] text-slate-400 font-medium">
          {label}
        </span>
      )}
    </div>
  );
}
