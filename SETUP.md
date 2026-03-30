# Quick Start Guide

## Prerequisites
- Node.js 20+ (or use the version specified in package.json)
- Python 3.8+
- npm or yarn
- 500MB free disk space

## Installation & Setup

### 1. Backend + Python ML (5 min)

```bash
# Navigate to project root
cd c:\Users\Asif Computer\OneDrive\Desktop\AI_Data_Dashboard

# Install Node dependencies
npm install

# Activate Python virtual environment
.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
npm start
# Expected output: "Express server running on http://localhost:5000"
```

**Keep this terminal open.**

---

### 2. Frontend (5 min)

**Open a NEW terminal window:**

```bash
# Navigate to frontend
cd c:\Users\Asif Computer\OneDrive\Desktop\AI_Data_Dashboard\frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Expected output: "Local: http://localhost:3000"
```

**Keep this terminal open.**

---

### 3. Verify It Works (2 min)

1. Open browser → `http://localhost:3000`
2. You should see: **"Employee Salary Prediction Dashboard"**
3. Create a test CSV file with content:
   ```csv
   Name,Age,Salary,Department
   Alice,28,65000,Engineering
   Bob,35,85000,Sales
   Carol,32,75000,Marketing
   ```
4. Upload the file
5. Wait for processing (2-5 seconds)
6. You should see:
   - Summary cards (3 employees, avg age, avg salary, etc.)
   - Scatter chart showing Age vs Predicted Salary
   - Department bar chart
   - Results table with predictions

✅ **System is working!**

---

## Common Issues & Fixes

### Issue: "Network error: unable to reach backend"
**Solution:**
- Check backend is running on port 5000: `curl http://localhost:5000`
- Check `NEXT_PUBLIC_API_BASE_URL` in frontend environment
- Ensure both servers are running in separate terminals

### Issue: "CSV file is empty" or "Invalid JSON from Python script"
**Solution:**
- Ensure CSV has all required columns: `Name`, `Age`, `Salary`, `Department`
- Age and Salary must be numeric
- File size must be < 10MB

### Issue: "PYTHON_PATH not found"
**Solution:**
- The backend looks for python using system PATH
- If it fails, set explicit path:
  ```bash
  # Windows
  $env:PYTHON_PATH = "C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe"
  npm start
  ```

### Issue: "ModuleNotFoundError: No module named 'pandas'"
**Solution:**
```bash
# Make sure you activated the virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Mac/Linux

# Then reinstall
pip install -r requirements.txt
```

---

## Optional: Streamlit Dashboard (Dev Tool)

Use Streamlit for interactive data exploration (NOT the main dashboard):

```bash
# Requires Python venv activated
.venv\Scripts\Activate.ps1

# Install Streamlit (already in requirements.txt)
streamlit run app.py
# Opens at http://localhost:8501
```

**Note:** This is a development tool. The main production dashboard is the Next.js app at `http://localhost:3000`.

---

## Project Structure Reference

```
AI_Data_Dashboard/
├── frontend/              ← Next.js app (UI)
│   └── app/
│       └── page.tsx      ← Main dashboard (what users see)
├── server.js             ← Express backend (API)
├── ml_model.py           ← Python ML engine
├── ARCHITECTURE.md       ← Detailed architecture docs
└── SETUP.md             ← This file
```

---

## Stopping the Servers

**In each terminal:**
```bash
# Press Ctrl+C to stop the server
```

---

## Environment Variables (Optional)

Create `.env.local` in the `frontend/` directory:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

For production, set this to your deployed backend URL.

---

## Next Steps

1. ✅ Backend running on port 5000
2. ✅ Frontend running on port 3000
3. ✅ Upload test CSV
4. → Explore dashboard features
5. → Check ARCHITECTURE.md for full details
6. → See bottom of this file for deployment notes

---

## Deployment Notes

### Current Status
- **Backend:** Containerized (Dockerfile) for Render/Docker deployment
- **Frontend:** Not yet deployed - remains local development only

### To Enable Full-Stack Deployment
1. Deploy frontend separately (Vercel, Netlify, etc.) OR add to Docker
2. Set `NEXT_PUBLIC_API_BASE_URL` to deployed backend URL
3. Update `render.yaml` to include frontend build

See `ARCHITECTURE.md` for full deployment instructions.

---

## Support

For detailed component information, see `ARCHITECTURE.md`.

For architecture diagram and data flow, see `ARCHITECTURE.md`.

For troubleshooting complex issues, check server logs:
- Backend logs: Terminal where you ran `npm start`
- Frontend logs: Browser console (F12) and terminal where you ran `npm run dev`
