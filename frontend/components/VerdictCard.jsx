"use client";

/**
 * VerdictCard — Displays an AI analysis verdict with risk level, score,
 * explanation, and recommended actions.
 *
 * Props:
 *   result — { risk_level, risk_score, scam_type, explanation, matched_signals?, source?,
 *              synthetic_voice_probability?, feature_checklist?, authentic? }
 */

import { RISK_COLORS } from "@/lib/mock-data";
import RiskGauge from "./RiskGauge";
import { AlertTriangle, CheckCircle, ShieldAlert, Info } from "lucide-react";

export default function VerdictCard({ result }) {
  if (!result) return null;

  const risk = result.risk_level || "LOW";
  const score = result.risk_score || 0;
  const color = RISK_COLORS[risk] || "#888";

  return (
    <div
      className="verdict-panel animate-in"
      style={{
        "--risk-color": color,
        "--risk-glow": `${color}10`,
      }}
    >
      <div className="relative z-10 space-y-4">
        {/* Header: Risk + Gauge */}
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              {risk === "CRITICAL" || risk === "HIGH" ? (
                <ShieldAlert className="w-5 h-5" style={{ color }} />
              ) : (
                <CheckCircle className="w-5 h-5" style={{ color }} />
              )}
              <span
                className="text-lg font-extrabold tracking-tight"
                style={{ color }}
              >
                {risk} RISK
              </span>
            </div>
            <p className="text-sm text-slate-300">
              <span className="text-slate-500">Type: </span>
              <span className="font-semibold">
                {result.scam_type ||
                  (result.authentic ? "Authentic" : "Unknown")}
              </span>
            </p>
          </div>
          <RiskGauge score={score} risk={risk} size={80} />
        </div>

        {/* Progress bar */}
        <div className="risk-progress">
          <div
            className="risk-progress-fill"
            style={{
              width: `${Math.min(score, 100)}%`,
              background: `linear-gradient(90deg, ${color}88, ${color})`,
            }}
          />
        </div>

        {/* Synthetic voice probability (audio) */}
        {result.synthetic_voice_probability !== undefined && (
          <div className="flex items-center gap-3 p-3 rounded-lg bg-base-600/50">
            <Info className="w-4 h-4 text-accent-blue flex-shrink-0" />
            <div>
              <p className="text-xs text-slate-400">
                Synthetic voice probability
              </p>
              <p className="text-sm font-bold text-slate-100">
                {(result.synthetic_voice_probability * 100).toFixed(0)}%
              </p>
            </div>
          </div>
        )}

        {/* Matched signals (text analysis) */}
        {result.matched_signals?.length > 0 && (
          <div className="flex flex-wrap gap-2">
            <span className="text-xs text-slate-500 font-medium">
              Signals:
            </span>
            {result.matched_signals.map((s) => (
              <span
                key={s}
                className="px-2 py-0.5 rounded-full text-xs font-semibold bg-accent-blue/10 text-accent-blue border border-accent-blue/20"
              >
                {s}
              </span>
            ))}
          </div>
        )}

        {/* Feature checklist (counterfeit) */}
        {result.feature_checklist && (
          <div className="space-y-1.5">
            <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">
              Security Feature Checklist
            </p>
            {Object.entries(result.feature_checklist).map(([feature, ok]) => (
              <div
                key={feature}
                className="flex items-center gap-2 text-sm"
              >
                <span className={ok ? "text-risk-low" : "text-risk-critical"}>
                  {ok ? "✅" : "❌"}
                </span>
                <span className="text-slate-300">{feature}</span>
              </div>
            ))}
          </div>
        )}

        {/* Explanation */}
        <div className="p-3 rounded-lg bg-base-600/30 border border-base-400/50">
          <p className="text-sm text-slate-300 leading-relaxed">
            <span className="font-semibold text-slate-200">
              Verdict explanation:{" "}
            </span>
            {result.explanation}
          </p>
        </div>

        {/* High risk action */}
        {(risk === "CRITICAL" || risk === "HIGH") && (
          <div className="flex items-start gap-3 p-3 rounded-lg bg-risk-critical/8 border border-risk-critical/20">
            <AlertTriangle className="w-5 h-5 text-risk-critical flex-shrink-0 mt-0.5" />
            <div className="text-sm text-slate-200">
              <strong>⚠️ Recommended action:</strong> Disconnect immediately. Do
              NOT pay or share OTP/UPI PIN. Call the Cyber Crime Helpline{" "}
              <strong className="text-risk-critical">1930</strong> and report at{" "}
              <span className="text-accent-blue">cybercrime.gov.in</span>.
            </div>
          </div>
        )}

        {/* Source indicator */}
        {result.source === "mock" && (
          <p className="text-[0.7rem] text-slate-500 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-accent-purple" />
            Result generated in offline Demo Mode (no backend connected)
          </p>
        )}
      </div>
    </div>
  );
}
