# Vercel (Next.js frontend)

1. Import the repo at https://vercel.com/new.
2. Set **Root Directory** to `frontend`.
3. Framework preset: **Next.js** (auto-detected).
4. Environment variables:
   - `NEXT_PUBLIC_API_BASE_URL` → your deployed backend URL.
   - `NEXT_PUBLIC_MAPBOX_TOKEN` → your Mapbox public token.
5. Deploy. Every push to the main branch redeploys automatically.

Tip: use a **preview** branch while iterating, then promote to production once
stable so the demo URL never breaks.
