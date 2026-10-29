# AI-Powered Multimodal Construction Intelligence Platform

A student-project demo built with **React + Vite** and **FastAPI**. It includes a dashboard and working demo flows for:
- Site safety monitoring (image upload + demo analysis)
- Crack detection and severity guidance (image upload + demo analysis)
- Real-estate valuation estimate
- Construction project planning
- Daily site assistant
- Weather-aware advisory (demo weather data)
- Construction knowledge assistant

> **Important:** This is a local prototype. AI outputs are simulated/demo logic, not certified engineering or safety advice. It does not connect to a real multimodal LLM or live weather service yet. Use a qualified site professional for real decisions.

## Requirements
- Python 3.10+
- Node.js 18+
- npm

## Run on Windows
### 1) Start the FastAPI backend
Open a terminal in the project folder:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

API docs: http://127.0.0.1:8000/docs

### 2) Start the React frontend
Open a **second terminal**:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL shown by Vite, usually http://localhost:5173.

## Run on macOS / Linux
Backend:
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Frontend:
```bash
cd frontend
npm install
npm run dev
```

## API endpoints
- `GET /api/health`
- `POST /api/analyze/safety` (multipart image)
- `POST /api/analyze/crack` (multipart image)
- `POST /api/valuation`
- `POST /api/plan`
- `POST /api/assistant`
- `POST /api/weather-advice`
- `POST /api/knowledge`

## Connect a real multimodal model later
Replace the demo logic in `backend/main.py` with a model provider call. Keep responses validated against stable JSON schemas, and store API keys in environment variables (never commit secrets). Add authentication, logging, rate limits, privacy controls, and professional validation before production use.
