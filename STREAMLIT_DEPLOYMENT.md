# Streamlit Deployment Guide

Last updated: April 1, 2026

## Scope

This deploys the Streamlit dashboard from `app.py`.

- Deploy target: Streamlit Community Cloud
- App URL result: `https://<your-app-name>.streamlit.app`
- Note: The separate Next.js frontend in `frontend/` is not used in this deployment mode.

## 1. Pre-Deployment Checklist

Confirm these files are in the repository root:

- `app.py` (Streamlit entrypoint)
- `requirements.txt` (Python packages)
- `runtime.txt` (Python version for cloud)
- `.streamlit/config.toml` (Streamlit runtime config)

## 2. Push to GitHub

If your latest local changes are not on GitHub yet, commit and push:

```bash
git add .
git commit -m "Add Streamlit deployment config and docs"
git push
```

## 3. Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/
2. Click **Create app**.
3. Choose your GitHub repository.
4. Set:
   - Branch: `main` (or your deploy branch)
   - Main file path: `app.py`
5. Click **Deploy**.

## 4. Verify Deployment

After deployment completes:

1. Open your Streamlit app URL.
2. Upload `test_data.csv`.
3. Validate:
   - File uploads successfully
   - Overview, Insights, Predictions, and Visualizations render
   - Salary prediction works

## 5. Updating the App

Any push to the selected branch triggers automatic redeploy.

## 6. Troubleshooting

### Build fails due to package install

- Check `requirements.txt` for typos.
- Re-run locally:

```bash
& "c:/Users/Asif Computer/OneDrive/Desktop/AI_Data_Dashboard/.venv/Scripts/python.exe" -m pip install -r requirements.txt
```

### App starts but page errors on upload

- Ensure uploaded CSV has expected columns used by the app (`Name`, `Age`, `Salary`, `Department` for full feature coverage).

### Python version mismatch

- `runtime.txt` pins cloud Python to `3.11.9`.
- If needed, change version and redeploy.

## 7. Local Run Command (Verified)

```bash
& "c:/Users/Asif Computer/OneDrive/Desktop/AI_Data_Dashboard/.venv/Scripts/python.exe" -m streamlit run app.py
```

This command was validated in this workspace.
