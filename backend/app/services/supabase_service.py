"""
Service: Supabase (PostgreSQL) wrapper — mock report logging & dashboard data.

Tables (proposed)
-----------------
fraud_reports(id, created_at, source, scam_type, risk_score, verdict,
              lang, entity_meta jsonb, lat, lng, status)

Functions (planned)
-------------------
- log_report(report)      -> insert a new fraud report.
- list_reports(filters)   -> for the dashboard table.
- get_stats()             -> aggregate counts / trends.
- get_hotspots()          -> lat/lng points for the Mapbox map.

Design notes
------------
- Uses supabase-py client with SUPABASE_URL + SUPABASE_KEY.
- Keep all persistence here so routes stay thin.

TODO
----
[ ] Implement CRUD + aggregation helpers.
[ ] Provide an in-memory fallback for offline demo mode.
"""
