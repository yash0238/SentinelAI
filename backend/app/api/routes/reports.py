"""
Route: Reports & dashboard data.

Endpoints (planned)
-------------------
GET  /reports              -> list logged fraud reports (for the dashboard).
GET  /reports/stats        -> aggregate stats (counts by type, trend, hotspots).
GET  /reports/hotspots     -> geo-coordinates for the Mapbox "Active Digital
                            Arrests" map on the police dashboard.
POST /reports              -> log a new mock report (Supabase).

TODO
----
[ ] Define APIRouter(prefix="/reports", tags=["Reports"]).
[ ] CRUD against Supabase table `fraud_reports`.
[ ] Aggregation queries for stats/hotspots.
"""
