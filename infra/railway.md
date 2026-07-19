# Railway (backend alternative to Render)

1. Create a project at https://railway.app → **Deploy from GitHub repo**.
2. Set the **root directory** to `backend`.
3. Railway auto-detects Python. Set the start command:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add all env vars from `.env.example` under **Variables**.
5. Deploy and copy the generated public URL.

Railway also offers one-click **Redis** and **Postgres** plugins if you prefer
to keep everything on one platform instead of Upstash/Supabase.
