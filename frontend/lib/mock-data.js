/**
 * SentinelAI — Mock data provider.
 *
 * Mirrors the Streamlit mock_data.py so the Next.js dashboard can demo fully
 * WITHOUT a running backend. Every function returns the same shape the real
 * backend endpoints will return.
 *
 * All data is synthetic. No real victim PII.
 */

// --- Seeded random (deterministic for stable demo) -------------------------

let _seed = 42;
function seededRandom() {
  _seed = (_seed * 16807 + 0) % 2147483647;
  return (_seed - 1) / 2147483646;
}
function randInt(min, max) {
  return Math.floor(seededRandom() * (max - min + 1)) + min;
}
function pick(arr) {
  return arr[Math.floor(seededRandom() * arr.length)];
}
function weightedPick(items, weights) {
  const total = weights.reduce((a, b) => a + b, 0);
  let r = seededRandom() * total;
  for (let i = 0; i < items.length; i++) {
    r -= weights[i];
    if (r <= 0) return items[i];
  }
  return items[items.length - 1];
}

// --- Constants -------------------------------------------------------------

export const SCAM_TYPES = [
  "Digital Arrest (fake CBI/ED)",
  "Fake Courier / Customs",
  "KYC / Bank Update",
  "OTP / UPI Phishing",
  "Investment / Trading",
  "Loan App Extortion",
  "Electricity Disconnection",
  "Job / Work-from-home",
];

export const LANGUAGES = [
  "Hindi",
  "English",
  "Marathi",
  "Tamil",
  "Telugu",
  "Bengali",
  "Kannada",
];

export const CITIES = [
  { name: "Delhi", lat: 28.6139, lng: 77.209 },
  { name: "Mumbai", lat: 19.076, lng: 72.8777 },
  { name: "Bengaluru", lat: 12.9716, lng: 77.5946 },
  { name: "Hyderabad", lat: 17.385, lng: 78.4867 },
  { name: "Chennai", lat: 13.0827, lng: 80.2707 },
  { name: "Kolkata", lat: 22.5726, lng: 88.3639 },
  { name: "Pune", lat: 18.5204, lng: 73.8567 },
  { name: "Jaipur", lat: 26.9124, lng: 75.7873 },
  { name: "Ahmedabad", lat: 23.0225, lng: 72.5714 },
  { name: "Lucknow", lat: 26.8467, lng: 80.9462 },
  { name: "Nagpur", lat: 21.1458, lng: 79.0882 },
  { name: "Patna", lat: 25.5941, lng: 85.1376 },
];

const STATUSES = ["New", "Under Review", "Escalated", "Resolved"];
const SOURCES = ["WhatsApp", "IVR", "Dashboard"];

// --- Risk helpers ----------------------------------------------------------

export function scoreToRisk(score) {
  if (score >= 85) return "CRITICAL";
  if (score >= 65) return "HIGH";
  if (score >= 40) return "MEDIUM";
  return "LOW";
}

export const RISK_COLORS = {
  CRITICAL: "#ff2e63",
  HIGH: "#ff7f0e",
  MEDIUM: "#f4c430",
  LOW: "#2ecc71",
};

export const NODE_COLORS = {
  victim: "#4da6ff",
  suspect: "#ff2e63",
  phone: "#f4c430",
  upi: "#a66bff",
  device: "#2ecc71",
  ip: "#00d0d0",
};

// --- Data generators -------------------------------------------------------

export function getStats() {
  return {
    active_sessions: 18,
    high_risk_today: 47,
    total_reports: 1284,
    counterfeit_flags: 63,
    amount_saved_cr: 12.4,
    avg_detection_seconds: 3.2,
  };
}

export function getReports(n = 60) {
  _seed = 42; // Reset for determinism
  const now = Date.now();
  const reports = [];
  for (let i = 0; i < n; i++) {
    const city = pick(CITIES);
    const risk = weightedPick(
      ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
      [15, 35, 30, 20]
    );
    const scoreRanges = {
      CRITICAL: [88, 99],
      HIGH: [70, 87],
      MEDIUM: [45, 69],
      LOW: [5, 44],
    };
    const [sMin, sMax] = scoreRanges[risk];
    const createdAt = new Date(now - randInt(1, 4320) * 60000);
    reports.push({
      id: `SA-${10000 + i}`,
      created_at: createdAt.toISOString().slice(0, 16).replace("T", " "),
      scam_type: pick(SCAM_TYPES),
      risk_level: risk,
      risk_score: randInt(sMin, sMax),
      language: pick(LANGUAGES),
      source: pick(SOURCES),
      city: city.name,
      lat: city.lat + (seededRandom() - 0.5) * 0.1,
      lng: city.lng + (seededRandom() - 0.5) * 0.1,
      amount_involved: pick([0, 25000, 50000, 120000, 300000, 750000]),
      status: pick(STATUSES),
    });
  }
  return reports;
}

export function getHotspots() {
  _seed = 99;
  return CITIES.map((city) => {
    const count = randInt(8, 120);
    return {
      city: city.name,
      lat: city.lat,
      lng: city.lng,
      count,
      risk: count > 90 ? "CRITICAL" : count > 50 ? "HIGH" : "MEDIUM",
    };
  });
}

export function getScamTrend(days = 14) {
  _seed = 77;
  const now = Date.now();
  const trend = [];
  let base = 40;
  for (let d = days; d > 0; d--) {
    base += randInt(-6, 10);
    base = Math.max(10, base);
    const date = new Date(now - d * 86400000);
    trend.push({
      date: date.toLocaleDateString("en-US", { month: "short", day: "numeric" }),
      reports: base,
    });
  }
  return trend;
}

export function getScamTypeBreakdown() {
  _seed = 55;
  return SCAM_TYPES.map((t) => ({
    scam_type: t,
    count: randInt(40, 260),
  }));
}

export function getClusters() {
  return {
    cluster_id: "RING-007",
    nodes: [
      { id: "V1", label: "Victim A", type: "victim" },
      { id: "V2", label: "Victim B", type: "victim" },
      { id: "V3", label: "Victim C", type: "victim" },
      { id: "P1", label: "+91 98••• 210", type: "phone" },
      { id: "P2", label: "+91 90••• 774", type: "phone" },
      { id: "U1", label: "mule1@upi", type: "upi" },
      { id: "U2", label: "mule2@upi", type: "upi" },
      { id: "U3", label: "collector@upi", type: "upi" },
      { id: "D1", label: "Device 4F:A2", type: "device" },
      { id: "S1", label: "Suspect X", type: "suspect" },
    ],
    edges: [
      { source: "V1", target: "P1", label: "received call" },
      { source: "V2", target: "P1", label: "received call" },
      { source: "V3", target: "P2", label: "received call" },
      { source: "P1", target: "D1", label: "linked device" },
      { source: "P2", target: "D1", label: "linked device" },
      { source: "V1", target: "U1", label: "transferred" },
      { source: "V2", target: "U2", label: "transferred" },
      { source: "V3", target: "U2", label: "transferred" },
      { source: "U1", target: "U3", label: "funneled" },
      { source: "U2", target: "U3", label: "funneled" },
      { source: "D1", target: "S1", label: "operated by" },
      { source: "U3", target: "S1", label: "controlled by" },
    ],
  };
}

// --- Live demo analysis mocks -----------------------------------------------

export function analyzeText(text) {
  const lower = (text || "").toLowerCase();
  const signals = {
    arrest: [
      "arrest",
      "cbi",
      "ed ",
      "narcotics",
      "police case",
      "money laundering",
      "custody",
    ],
    courier: ["parcel", "courier", "customs", "fedex", "seized"],
    kyc: ["kyc", "account block", "verify your account", "pan card"],
    otp: ["otp", "upi pin", "share code", "cvv"],
    urgency: [
      "urgent",
      "immediately",
      "arrest warrant",
      "do not disconnect",
      "within 1 hour",
    ],
  };

  let score = 0;
  const matched = [];
  for (const [label, kws] of Object.entries(signals)) {
    for (const kw of kws) {
      if (lower.includes(kw)) {
        score += 18;
        matched.push(label);
        break;
      }
    }
  }
  score = Math.min(score, 99);

  const scamType = matched.includes("arrest")
    ? "Digital Arrest (fake CBI/ED)"
    : matched.includes("courier")
      ? "Fake Courier / Customs"
      : matched.includes("otp")
        ? "OTP / UPI Phishing"
        : matched.includes("kyc")
          ? "KYC / Bank Update"
          : "Likely Legitimate";

  const risk = scoreToRisk(score);
  return {
    risk_level: risk,
    risk_score: score,
    scam_type: scamType,
    matched_signals: [...new Set(matched)].sort(),
    explanation: explainVerdict(risk, scamType),
    source: "mock",
  };
}

export function analyzeAudio(filename) {
  const fn = (filename || "").toLowerCase();
  const synthetic = ["synthetic", "fake", "clone", "ai"].some((k) =>
    fn.includes(k)
  );
  const prob = synthetic ? 0.94 : 0.11;
  const score = synthetic ? 94 : 22;
  const risk = scoreToRisk(synthetic ? score : 20);
  return {
    risk_level: risk,
    risk_score: score,
    synthetic_voice_probability: prob,
    scam_type: synthetic
      ? "Digital Arrest (fake CBI/ED)"
      : "Likely Legitimate",
    explanation: synthetic
      ? "High probability of an AI-generated voice combined with a coercive script — consistent with a live digital-arrest scam."
      : "Voice appears human and no coercive script detected.",
    source: "mock",
  };
}

export function analyzeImage(filename) {
  const fn = (filename || "").toLowerCase();
  const fake = ["fake", "counterfeit", "forged"].some((k) => fn.includes(k));
  const checklist = {
    Microprint: !fake,
    "Security thread": !fake,
    "Serial-number pattern": !fake,
    "Intaglio print texture": !fake,
    Watermark: true,
  };
  const passed = Object.values(checklist).filter(Boolean).length;
  const score = Math.round((1 - passed / Object.keys(checklist).length) * 100);
  return {
    authentic: !fake,
    risk_level: scoreToRisk(score),
    risk_score: score,
    feature_checklist: checklist,
    explanation: fake
      ? "Multiple security features failed verification — flag for manual inspection."
      : "All key security features verified.",
    source: "mock",
  };
}

function explainVerdict(risk, scamType) {
  if (risk === "CRITICAL" || risk === "HIGH") {
    return `This matches a known ${scamType} pattern. Do not pay, share OTP/UPI PIN, or stay on the call. Disconnect and call 1930.`;
  }
  if (risk === "MEDIUM") {
    return "Some suspicious markers present. Stay cautious and verify independently.";
  }
  return "No strong scam markers detected. Remain alert and never share OTPs.";
}
