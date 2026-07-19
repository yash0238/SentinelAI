/**
 * SentinelAI Dashboard — Home.
 *
 * Judge-facing landing screen. Composition (planned):
 *   - Row of StatCards: active sessions, high-risk alerts today, reports,
 *     counterfeit flags.
 *   - HotspotMap: Mapbox map with live "Active Digital Arrests" markers,
 *     pulling from GET /reports/hotspots.
 *   - Recent high-risk alerts feed.
 *
 * TODO
 *   [ ] Fetch stats via lib/api.js (SWR).
 *   [ ] Lay out with Tailwind grid; keep it clean and high-contrast.
 */
