# Dashboard components

Reusable UI pieces. Build in this order (most demo impact first):

1. `StatCard.jsx` — KPI cards for the header row.
2. `HotspotMap.jsx` — Mapbox map of active digital arrests (the wow moment).
3. `ReportsTable.jsx` — filterable report list.
4. `NetworkGraph.jsx` — money-mule cluster visualisation.
5. `RiskGauge.jsx` — risk-score dial for detail views.

Keep components presentational; fetch data in the page and pass props down.
