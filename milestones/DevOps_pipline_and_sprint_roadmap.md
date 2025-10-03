[ DAY 1–2 ] ───────────────────────────────────────────────
 PLAN & ALIGN
 ┌─────────────────────────────────────────────────────────┐
 │ • Finalize problem statement & user stories             │
 │ • Map NASA + local datasets (Douala, Lagos, Pune)       │
 │ • Agree on Core + Local module architecture             │
 │ • Set up Trello/Jira board, Notion docs, Slack channels │
 └─────────────────────────────────────────────────────────┘
           │
           ▼
[ DAY 3–5 ] ───────────────────────────────────────────────
 CODE & COLLAB
 ┌─────────────────────────────────────────────────────────┐
 │ • Initialize GitHub repo & branching strategy           │
 │ • Scaffold React + Mapbox frontend                      │
 │ • Scaffold Node.js/Express (or FastAPI) backend          │
 │ • Set up PostGIS database in cloud                      │
 │ • Connect NASA APIs (MODIS, Landsat, GPM, SMAP)          │
 └─────────────────────────────────────────────────────────┘
           │
           ▼
[ DAY 6–7 ] ───────────────────────────────────────────────
 BUILD & TEST
 ┌─────────────────────────────────────────────────────────┐
 │ • Configure GitHub Actions CI pipeline                  │
 │ • Add linting, unit tests (Jest/Pytest)                  │
 │ • Build Docker images for frontend & backend            │
 │ • First integration test: NASA data → API → Map layer   │
 └─────────────────────────────────────────────────────────┘
           │
           ▼
[ DAY 8–9 ] ───────────────────────────────────────────────
 DEPLOY & DEMO (STAGING)
 ┌─────────────────────────────────────────────────────────┐
 │ • Deploy frontend to Vercel/Netlify                     │
 │ • Deploy backend to AWS/Heroku                          │
 │ • Connect staging DB + PostGIS                          │
 │ • Share live staging link for team feedback             │
 └─────────────────────────────────────────────────────────┘
           │
           ▼
[ DAY 10–11 ] ─────────────────────────────────────────────
 MONITOR & ITERATE
 ┌─────────────────────────────────────────────────────────┐
 │ • Add Grafana dashboards for API & DB metrics           │
 │ • Set up ELK logging                                    │
 │ • Collect tester feedback from planners & teammates     │
 │ • Fix bugs, improve UI/UX                               │
 └─────────────────────────────────────────────────────────┘
           │
           ▼
[ DAY 12–13 ] ─────────────────────────────────────────────
 DATA OPS FINALIZATION
 ┌─────────────────────────────────────────────────────────┐
 │ • Automate NASA data ingestion (cron jobs / Lambda)     │
 │ • Preprocess imagery with Python (rasterio, geopandas)  │
 │ • Push processed tiles to S3 → serve via Mapbox         │
 │ • Validate Douala, Lagos, Pune modules                  │
 └─────────────────────────────────────────────────────────┘
           │
           ▼
[ DAY 14 ] ────────────────────────────────────────────────
 FINAL DEMO & SUBMISSION
 ┌─────────────────────────────────────────────────────────┐
 │ • Freeze code on main branch                            │
 │ • Deploy production build                               │
 │ • Prepare pitch deck + live demo                        │
 │ • Submit to NASA Space Apps portal                      │
 └─────────────────────────────────────────────────────────┘
