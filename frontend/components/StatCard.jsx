"use client";

/**
 * StatCard — Glassmorphic KPI card with accent top-border and icon.
 *
 * Props:
 *   value   — display value (string | number)
 *   label   — description text
 *   icon    — Lucide icon component
 *   accent  — CSS color string for the accent
 *   delay   — stagger animation index (1–6)
 */
export default function StatCard({ value, label, icon: Icon, accent = "#4da6ff", delay = 0 }) {
  return (
    <div
      className={`stat-card animate-in ${delay ? `stagger-${delay}` : ""}`}
      style={{ "--accent-color": accent }}
    >
      <div className="flex items-start justify-between">
        <div>
          <p
            className="text-2xl font-extrabold tracking-tight"
            style={{ color: accent }}
          >
            {value}
          </p>
          <p className="text-[0.78rem] text-slate-400 mt-1 font-medium">
            {label}
          </p>
        </div>
        {Icon && (
          <div
            className="p-2 rounded-lg"
            style={{ background: `${accent}15` }}
          >
            <Icon
              className="w-5 h-5"
              style={{ color: accent }}
            />
          </div>
        )}
      </div>
    </div>
  );
}
