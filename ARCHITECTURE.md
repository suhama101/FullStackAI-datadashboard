# AI Data Dashboard - Clean Full-Stack Architecture

## Overview

This is a **single, unified full-stack architecture** for an AI-powered employee salary prediction dashboard. The system follows a clear separation of concerns with a modern tech stack.

```
┌─────────────────────────────────────────────────────────┐
│  Frontend: Next.js (App Router - TypeScript)            │
│  Location: /frontend/app/page.tsx                       │
│  Port: 3000                                             │
│  Features: CSV upload, visualizations, metrics cards    │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP POST /predict
                     │ (FormData: CSV file)
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Backend: Express.js (Node.js)                          │
│  Location: server.js                                    │
│  Port: 5000                                             │
│  Endpoints: GET /, POST /predict                        │
│  Responsibilities:                                      │
│  - File upload handling (multer)                        │
│  - CORS & routing                                       │
│  - Python ML execution                                  │
└────────────────────┬────────────────────────────────────┘
                     │ spawn process
                     │ (csv file path)
                     ▼
┌─────────────────────────────────────────────────────────┐
│  ML Engine: Python (scikit-learn)                       │
│  Location: ml_model.py                                  │
│  Responsibilities:                                      │
│  - CSV validation against required columns             │
│  - Data cleaning & type conversion                      │
│  - Linear regression model training                     │
│  - Salary predictions for employees                     │
│  Input: CSV file (Name, Age, Salary, Department)       │
│  Output: JSON with predictions                          │
└─────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
AI_Data_Dashboard/
├── frontend/                    # Next.js application (main UI)
│   ├── app/
│   │   ├── page.tsx            # Main dashboard page (ACTIVE)
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── public/                 # Static assets
│   ├── package.json            # Frontend dependencies
│   └── next.config.ts          # Next.js config
│
├── server.js                    # Express backend (PORT 5000)
├── ml_model.py                  # ML pipeline (called by server.js)
├── requirements.txt             # Python dependencies
│
├── Dockerfile                   # Container build (backend only)
├── render.yaml                  # Deployment config (currently incomplete)
│
├── ARCHITECTURE.md              # This file
├── SETUP.md                     # Development setup guide
│
├── [OPTIONAL DEV TOOLS]
├── app.py                       # Streamlit dashboard (dev tool only - optional)
├── model.py                     # Analysis functions (used by app.py)
├── utils.py                     # Data cleaning helpers (used by app.py)
│
└── package.json                 # Root dependencies (backend only)
```

---

## Component Details

### 1. Frontend (Next.js App Router)
**File:** `frontend/app/page.tsx`
**Status:** ✅ ACTIVE - Primary user interface

**Key Features:**
- CSV file upload with validation
- Real-time loading states
- Error handling with user-friendly messages
- Data visualization:
  - Scatter chart: Age vs. Predicted Salary
  - Bar chart: Employees by Department
  - Results table with all fields
- Summary metrics:
  - Total employees count
  - Average age
  - Average salary
  - Department count

**API Connection:**
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:5000";
const response = await axios.post(`${API_BASE_URL}/predict`, formData);
```

---

### 2. Backend (Express.js)
**File:** `server.js`
**Status:** ✅ ACTIVE - API and orchestration layer

**Routes:**
- **GET /**
  - Returns server health status
  - Message describing how to use the API

- **POST /predict**
  - Accepts multipart form data with a CSV file
  - Validates file (CSV only, max 10MB)
  - Writes file to tmp directory
  - Spawns Python process with file path
  - Returns JSON response:
    ```json
    {
      "success": true,
      "rows": 100,
      "model": {
        "coefficient": 5000.5,
        "intercept": 25000
      },
      "data": [
        {
          "Name": "John",
          "Age": 30,
          "Salary": 175000,
          "Department": "Engineering",
          "predicted_salary": 175002.5
        }
      ]
    }
    ```

**Error Handling:**
- Returns 400 status with error details for invalid CSV, missing fields, or ML failures
- Automatically cleans up temporary files after processing

---

### 3. ML Engine (Python)
**File:** `ml_model.py`
**Status:** ✅ ACTIVE - Predictive model

**Pipeline:**
1. **Validation:** Checks for required columns (Name, Age, Salary, Department)
2. **Cleaning:**
   - Strips whitespace from text columns
   - Converts Age and Salary to numeric types
   - Removes duplicate rows
   - Drops null values in critical fields
3. **Training:** Linear regression on Age → Salary
4. **Prediction:** Predicts salary for each employee based on age
5. **Output:** JSON with cleaned data + predictions

**Required CSV Columns:**
- `Name` (string)
- `Age` (numeric)
- `Salary` (numeric)
- `Department` (string)

---

## Optional Dev Tools

### Streamlit Dashboard (Development Only)
**File:** `app.py`
**Status:** ⚠️ OPTIONAL - Not part of main production flow

**Purpose:** Interactive data exploration tool for development and analysis.

**Features:**
- CSV upload
- Data overview & filtering
- ML predictions (Age → Salary)
- Data insights (correlations, statistics)
- Interactive visualizations (histograms, bar charts, boxplots)

**Run locally (dev only):**
```bash
cd c:\Users\Asif Computer\OneDrive\Desktop\AI_Data_Dashboard
.venv\Scripts\Activate.ps1
streamlit run app.py
```

**Note:** This is independent of the main Next.js + Express pipeline. Use it for exploratory analysis, not as part of the production dashboard.

---

## Data Flow

### Production Flow (What Users See)
1. User opens browser → `http://localhost:3000` (Next.js)
2. User selects CSV file and clicks "Upload and Predict"
3. Frontend sends POST request to `http://localhost:5000/predict`
4. Backend receives file, saves to temp location
5. Backend spawns Python process: `python ml_model.py /tmp/file.csv`
6. Python script:
   - Reads and validates CSV
   - Cleans data
   - Trains linear regression model
   - Returns JSON with predictions
7. Backend returns response to frontend
8. Frontend renders:
   - Summary cards (employee count, avg age, avg salary, dept count)
   - Scatter chart (age vs salary by department)
   - Bar chart (employees per department)
   - Results table (all fields including predictions)

---

## Environment Variables

### Frontend (`frontend/.env.local` or `.env.production`)
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000    # Dev
NEXT_PUBLIC_API_BASE_URL=https://yourdomain.com   # Production
```

### Backend (`server.js`)
```
PORT=5000                          # Defaults to 5000
PYTHON_PATH=python3                # Defaults to "python3" (Unix) or "python" (Windows)
NODE_ENV=production                # For Docker deployment
```

---

## Development Setup

### 1. Backend (Express + Python)
```bash
# Install Node dependencies
npm install

# Install Python dependencies (in virtual environment)
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Start backend
npm start
# Or: node server.js
# Server runs on http://localhost:5000
```

### 2. Frontend (Next.js)
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
# Frontend runs on http://localhost:3000
```

### 3. Verify Connection
- Open http://localhost:3000
- Upload a sample CSV with columns: Name, Age, Salary, Department
- Check browser console and backend logs for any errors

---

## Deployment

### Current State
- **Incomplete:** Only backend is containerized in `Dockerfile` and deployed via `render.yaml`
- **Missing:** Frontend deployment configuration

### What's Deployed
- Docker container with Node.js + Python
- Express API on port 5000
- Runs `npm start` (executes `server.js`)

### What's NOT Deployed
- Next.js frontend
- You must either:
  1. Deploy frontend separately (Vercel, Netlify, or similar)
  2. Add frontend build to Docker and serve via Express
  3. Use environment variable for `NEXT_PUBLIC_API_BASE_URL` pointing to deployed backend

### Recommended: Full Deployment
To enable full-stack deployment, add frontend build to Dockerfile:
```dockerfile
# Build frontend
FROM node:20 as frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend ./
RUN npm run build

# Build backend with frontend static files
FROM node:20 as backend
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY server.js ./
COPY ml_model.py ./
COPY requirements.txt ./
# Copy built frontend
COPY --from=frontend-builder /frontend/.next ./frontend/.next
COPY --from=frontend-builder /frontend/public ./frontend/public
# ... rest of backend setup
```

---

## Testing the System

### Test CSV (save as `test_data.csv`)
```csv
Name,Age,Salary,Department
Alice Johnson,28,65000,Engineering
Bob Smith,35,85000,Engineering
Carol White,32,75000,Sales
David Brown,45,95000,Management
Eve Davis,26,55000,Sales
```

### Test Command
```bash
# From project root
curl -X POST http://localhost:5000/predict \
  -F "file=@test_data.csv"
```

### Expected Response
```json
{
  "success": true,
  "rows": 5,
  "model": {
    "coefficient": 1200.5,
    "intercept": 20000
  },
  "data": [
    {
      "Name": "Alice Johnson",
      "Age": 28,
      "Salary": 65000,
      "Department": "Engineering",
      "predicted_salary": 53601.5
    },
    ...
  ]
}
```

Then open http://localhost:3000 in browser, upload the CSV, and see visualizations.

---

## Troubleshooting

### Frontend can't reach backend
- Check `http://localhost:5000` is running: `curl http://localhost:5000`
- Check `NEXT_PUBLIC_API_BASE_URL` environment variable in frontend
- Check CORS is enabled in `server.js`

### Python script fails
- Verify CSV has columns: Name, Age, Salary, Department
- Check Python dependencies: `pip install -r requirements.txt`
- Check PYTHON_PATH environment variable (should be `python3` or full path)

### File upload fails
- Max file size: 10MB
- Only CSV MIME types accepted: `text/csv`, `application/csv`, `application/vnd.ms-excel`
- Filename must include `.csv` extension

---

## Summary

✅ **Single Frontend:** Next.js in `frontend/app/page.tsx`  
✅ **Single API Backend:** Express in `server.js`  
✅ **Single ML Engine:** Python in `ml_model.py`  
✅ **Clear Data Flow:** Frontend → Backend → Python → Response → Visualization  
⚠️ **Optional Tools:** Streamlit dashboard available for dev/exploration only  
🚧 **Deployment:** Partial (backend only) - frontend deployment pending  

This architecture is clean, maintainable, and production-ready (with frontend deployment setup).
