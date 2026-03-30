const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs/promises");
const os = require("os");
const { spawn } = require("child_process");

const app = express();
const PORT = Number(process.env.PORT) || 5000;

const corsOrigins = (process.env.CORS_ORIGIN || "")
  .split(",")
  .map((origin) => origin.trim())
  .filter(Boolean);

app.use(
  cors({
    origin: (origin, callback) => {
      if (!origin || corsOrigins.length === 0 || corsOrigins.includes(origin)) {
        callback(null, true);
        return;
      }

      callback(new Error("CORS policy does not allow this origin."));
    },
  })
);

const uploadDir = path.join(os.tmpdir(), "ai_data_dashboard_uploads");
const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    try {
      await fs.mkdir(uploadDir, { recursive: true });
      cb(null, uploadDir);
    } catch (err) {
      cb(err);
    }
  },
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname) || ".csv";
    cb(null, `${Date.now()}-${Math.round(Math.random() * 1e9)}${ext}`);
  },
});

const upload = multer({
  storage,
  fileFilter: (req, file, cb) => {
    const isCsvName = file.originalname.toLowerCase().endsWith(".csv");
    const isCsvMime =
      file.mimetype === "text/csv" ||
      file.mimetype === "application/vnd.ms-excel" ||
      file.mimetype === "application/csv";

    if (isCsvName || isCsvMime) {
      cb(null, true);
      return;
    }

    cb(new Error("Only CSV files are allowed."));
  },
  limits: { fileSize: 10 * 1024 * 1024 },
});

function runPythonModel(csvPath) {
  return new Promise((resolve, reject) => {
    const defaultPython = process.platform === "win32" ? "python" : "python3";
    const pythonBin = process.env.PYTHON_PATH || defaultPython;
    const scriptPath = path.join(__dirname, "ml_model.py");
    const child = spawn(pythonBin, [scriptPath, csvPath], {
      cwd: __dirname,
    });

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    child.on("error", (err) => {
      reject(new Error(`Failed to start Python process: ${err.message}`));
    });

    child.on("close", (code) => {
      let parsed;
      try {
        parsed = JSON.parse(stdout);
      } catch (err) {
        const detail = stderr || stdout || "No output from Python script.";
        reject(new Error(`Invalid JSON from Python script. ${detail}`));
        return;
      }

      if (code !== 0) {
        const message = parsed.error || stderr || "Python script failed.";
        reject(new Error(message));
        return;
      }

      resolve(parsed);
    });
  });
}

app.get("/", (req, res) => {
  res.json({
    success: true,
    message: "Server is running. Use POST /predict with multipart/form-data and field 'file'.",
  });
});

app.post("/predict", upload.single("file"), async (req, res) => {
  let tempFilePath;

  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        error: "CSV file is required. Upload with field name 'file'.",
      });
    }

    tempFilePath = req.file.path;
    const result = await runPythonModel(tempFilePath);
    return res.status(200).json(result);
  } catch (err) {
    return res.status(400).json({
      success: false,
      error: err.message || "Prediction failed.",
    });
  } finally {
    if (tempFilePath) {
      try {
        await fs.unlink(tempFilePath);
      } catch (cleanupErr) {
        // Ignore cleanup errors to avoid masking API responses.
      }
    }
  }
});

app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(400).json({ success: false, error: err.message });
  }

  if (err) {
    return res.status(400).json({ success: false, error: err.message });
  }

  return next();
});

app.listen(PORT, () => {
  console.log(`Express server running on http://localhost:${PORT}`);
});
