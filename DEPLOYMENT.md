# Full-Stack Deployment Guide

Last updated: March 30, 2026

This project deploys as:
- Frontend (Next.js): Vercel
- Backend (Node.js + Python ML): Render

## 1. Deploy Backend on Render

### Option A: Blueprint deploy (recommended)
1. Push this repository to GitHub.
2. In Render, click New + > Blueprint.
3. Select the repository.
4. Render will detect `render.yaml` and create the backend service.
5. In service Environment settings, set or confirm:
   - `NODE_ENV=production`
   - `PYTHON_PATH=python3`
   - `CORS_ORIGIN=https://your-vercel-domain.vercel.app`
6. Deploy and wait for build completion.
7. Confirm backend health:
   - `GET https://<your-render-backend>.onrender.com/`

### Option B: Manual web service
1. In Render, click New + > Web Service.
2. Connect your GitHub repo.
3. Use Docker runtime and root Dockerfile (`Dockerfile`).
4. Set environment variables:
   - `NODE_ENV=production`
   - `PYTHON_PATH=python3`
   - `CORS_ORIGIN=https://your-vercel-domain.vercel.app`
5. Deploy and test `GET /`.

## 2. Deploy Frontend on Vercel

1. Push this repository to GitHub.
2. In Vercel, click Add New > Project.
3. Import this repository.
4. Set Root Directory to `frontend`.
5. Framework should auto-detect as Next.js.
6. Add environment variable:
   - `NEXT_PUBLIC_API_BASE_URL=https://<your-render-backend>.onrender.com`
7. Deploy.

## 3. Set Environment Variable NEXT_PUBLIC_API_BASE_URL

Set this variable in Vercel Project Settings > Environment Variables:
- Name: `NEXT_PUBLIC_API_BASE_URL`
- Value: `https://<your-render-backend>.onrender.com`

Important:
- Use `https`.
- Do not add a trailing slash.

The frontend already reads this variable in `frontend/app/page.tsx`.

## 4. Ensure Frontend Connects to Deployed Backend

After both deployments:
1. Open your Vercel app URL.
2. Upload a CSV file.
3. Verify the request goes to Render backend:
   - Browser DevTools > Network > `POST /predict`
   - Request URL should be `https://<your-render-backend>.onrender.com/predict`
4. Verify response contains:
   - `success: true`
   - `data` array with `predicted_salary`

If upload fails due to CORS:
1. Update Render `CORS_ORIGIN` to your exact Vercel domain.
2. If needed, include preview domains as comma-separated values:
   - `https://your-app.vercel.app,https://your-app-git-main-your-team.vercel.app`
3. Redeploy backend.

## 5. Production Checklist

- Backend URL works: `GET /` returns success JSON.
- Vercel env var `NEXT_PUBLIC_API_BASE_URL` is set.
- Render env var `CORS_ORIGIN` matches Vercel domain.
- CSV upload succeeds from deployed frontend.
- Table/charts/summary cards render with predicted results.

## 6. Fast Smoke Test

1. Backend test:
   - `curl https://<your-render-backend>.onrender.com/`
2. Frontend test:
   - Open `https://<your-vercel-app>.vercel.app`
3. End-to-end test:
   - Upload `test_data.csv`
   - Confirm records and charts appear.
