"""
SentinelAI — Streamlit dashboard (Python-only ALTERNATIVE to the Next.js app).

Pick ONE frontend. Streamlit is fastest if you want to stay entirely in Python
and spend your time on the AI backend; the Next.js app looks more polished for
judges. Delete whichever you don't use before the demo.

Planned tabs
------------
- Overview:   KPIs + a pydeck/Mapbox map of active digital-arrest hotspots.
- Live Demo:  upload a voice note / note image -> show the AI verdict live.
- Network:    fraud-ring cluster view (via the /graph endpoints).
- Reports:    table of logged reports.

Run: streamlit run app.py

TODO
----
[ ] Build tabs with st.tabs.
[ ] Call the FastAPI backend via requests using NEXT_PUBLIC_API_BASE_URL.
[ ] Use st.file_uploader for the live counterfeit/audio demo.
"""
