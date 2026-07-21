/**
 * SentinelAI Dashboard — API client helpers.
 *
 * Thin fetch wrappers around the FastAPI backend. Base URL comes from
 * NEXT_PUBLIC_API_BASE_URL. Falls back to mock data when the backend is
 * unreachable, so the dashboard ALWAYS works.
 */

import * as mock from "./mock-data";

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
const TIMEOUT_MS = 8000;

// --- Core fetch wrapper ----------------------------------------------------

async function apiFetch(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
    clearTimeout(timeout);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    clearTimeout(timeout);
    return null; // Caller uses mock fallback
  }
}

// --- Health check ----------------------------------------------------------

export async function backendOnline() {
  try {
    const res = await fetch(`${BASE_URL}/health`, {
      signal: AbortSignal.timeout(3000),
    });
    return res.ok;
  } catch {
    return false;
  }
}

// --- Dashboard data --------------------------------------------------------

export async function getStats() {
  const data = await apiFetch("/reports/stats");
  return data || mock.getStats();
}

export async function getReports(filters) {
  const params = new URLSearchParams();
  if (filters?.risk) params.set("risk", filters.risk);
  if (filters?.type) params.set("type", filters.type);
  if (filters?.source) params.set("source", filters.source);
  const qs = params.toString();
  const data = await apiFetch(`/reports${qs ? `?${qs}` : ""}`);
  return data || mock.getReports();
}

export async function getHotspots() {
  const data = await apiFetch("/reports/hotspots");
  return data || mock.getHotspots();
}

export function getScamTrend() {
  // No dedicated backend endpoint yet — always mock
  return mock.getScamTrend();
}

export function getScamTypeBreakdown() {
  return mock.getScamTypeBreakdown();
}

// --- Graph intelligence ----------------------------------------------------

export async function getClusters() {
  const data = await apiFetch("/graph/clusters");
  return data || mock.getClusters();
}

export async function getEntity(id) {
  const data = await apiFetch(`/graph/entity/${id}`);
  return data;
}

export async function getIntelPackage(clusterId) {
  const data = await apiFetch(`/graph/package/${clusterId}`);
  return data;
}

// --- Live demo analysis ----------------------------------------------------

export async function analyzeText(text) {
  const data = await apiFetch("/shield/chat", {
    method: "POST",
    body: JSON.stringify({ message: text }),
  });
  return data || mock.analyzeText(text);
}

export async function analyzeAudio(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${BASE_URL}/scam/analyze-audio`, {
      method: "POST",
      body: formData,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    return mock.analyzeAudio(file?.name || "");
  }
}

export async function analyzeImage(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const res = await fetch(`${BASE_URL}/counterfeit/verify`, {
      method: "POST",
      body: formData,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch {
    return mock.analyzeImage(file?.name || "");
  }
}
