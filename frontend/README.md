# SentinelAI — Frontend (Law-Enforcement Dashboard)

Next.js + Tailwind dashboard for officers: live "Active Digital Arrests" map,
fraud-network graph, and report analytics. Optimised to look polished for
judges in the demo.

## Quick start

```bash
cd frontend
npm install
cp .env.local.example .env.local   # add NEXT_PUBLIC_MAPBOX_TOKEN + API base
npm run dev
```

Open http://localhost:3000

## Planned pages / components

```
app/
├── layout.jsx                 # shell, nav, theme
├── page.jsx                   # dashboard home (KPIs + hotspot map)
├── network/page.jsx           # fraud-network graph explorer
└── reports/page.jsx           # reports table + filters

components/
├── HotspotMap.jsx             # Mapbox map of active digital arrests
├── RiskGauge.jsx              # risk-score visual
├── NetworkGraph.jsx           # money-mule cluster visualisation
├── StatCard.jsx               # KPI cards
└── ReportsTable.jsx           # sortable/filterable report list

lib/
└── api.js                     # typed fetch helpers to the FastAPI backend
```

## Notes

- Data comes from the backend `/reports`, `/reports/hotspots`, and
  `/graph/*` endpoints.
- Keep it to 3 focused screens — a polished narrow demo beats a broad,
  half-finished dashboard (see docs/HACKATHON_STRATEGY.md).

> Alternative: if you'd rather stay all-Python, a Streamlit dashboard lives in
> `frontend-streamlit/` — pick ONE and delete the other before the demo.
