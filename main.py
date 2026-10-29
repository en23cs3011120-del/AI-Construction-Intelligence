from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Construction Intelligence API", version="1.0.0",
              description="Demo API for an AI-powered construction intelligence student project.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class ValuationRequest(BaseModel):
    area_sqft: float = Field(gt=0)
    location: str = "Indore"
    property_type: str = "Residential"
    quality: str = "Standard"

class PlanRequest(BaseModel):
    project_name: str = "Residential Building"
    floors: int = Field(default=2, ge=1, le=100)
    area_sqft: float = Field(default=2000, gt=0)
    start_date: Optional[str] = None

class TextRequest(BaseModel):
    message: str
    context: Optional[str] = None

@app.get("/api/health")
def health():
    return {"status": "ok", "service": "Construction Intelligence API", "mode": "demo"}

async def image_result(file: UploadFile, kind: str):
    content = await file.read()
    if not content:
        return {"success": False, "error": "Uploaded file is empty."}
    if kind == "safety":
        return {
            "success": True, "filename": file.filename, "mode": "demo",
            "summary": "Demo screening completed. A human review is required before site action.",
            "risk_level": "Medium",
            "findings": [
                {"title": "PPE verification", "status": "Review", "detail": "Check that every worker in the image is wearing a helmet, high-visibility clothing, and appropriate footwear."},
                {"title": "Access and housekeeping", "status": "Review", "detail": "Inspect walking paths for loose materials, cables, and trip hazards."},
                {"title": "Edge protection", "status": "Priority check", "detail": "Verify guardrails and fall-protection controls around elevated edges."}
            ],
            "recommended_actions": ["Pause work if an immediate hazard is confirmed.", "Notify the site safety officer.", "Record the finding and re-check after corrective action."]
        }
    return {
        "success": True, "filename": file.filename, "mode": "demo",
        "summary": "Demo visual screening completed. This is not a structural diagnosis.",
        "severity": "Needs professional review",
        "findings": [
            {"title": "Visible surface feature", "status": "Inspect", "detail": "Review the marked area in good lighting and photograph it with a scale reference."},
            {"title": "Crack measurement", "status": "Not measured", "detail": "Measure width and length with a suitable gauge; note whether the crack is changing over time."},
            {"title": "Context needed", "status": "Required", "detail": "Record the element type, age, location, moisture exposure, and whether the crack is active."}
        ],
        "recommended_actions": ["Document and date the observation.", "Escalate wide, growing, diagonal, or structural-element cracks to a qualified engineer.", "Restrict access if there are signs of instability."]
    }

@app.post("/api/analyze/safety")
async def analyze_safety(file: UploadFile = File(...)):
    return await image_result(file, "safety")

@app.post("/api/analyze/crack")
async def analyze_crack(file: UploadFile = File(...)):
    return await image_result(file, "crack")

@app.post("/api/valuation")
def valuation(req: ValuationRequest):
    location_rates = {"Indore": 4200, "Bhopal": 3800, "Delhi": 7200, "Mumbai": 10500, "Pune": 6500}
    rate = location_rates.get(req.location.strip().title(), 4000)
    quality_factor = {"Basic": 0.85, "Standard": 1.0, "Premium": 1.35}.get(req.quality, 1.0)
    type_factor = {"Commercial": 1.2, "Residential": 1.0, "Plot": 0.65}.get(req.property_type, 1.0)
    low = req.area_sqft * rate * quality_factor * type_factor * 0.88
    high = req.area_sqft * rate * quality_factor * type_factor * 1.12
    return {"success": True, "mode": "illustrative estimate", "location": req.location,
            "area_sqft": req.area_sqft, "rate_per_sqft_used": round(rate*quality_factor*type_factor),
            "estimated_low_inr": round(low), "estimated_high_inr": round(high),
            "note": "Illustrative demo only; actual values depend on locality, land/title, age, amenities, and market data."}

@app.post("/api/plan")
def create_plan(req: PlanRequest):
    days = max(30, req.floors * 24 + int(req.area_sqft / 250))
    start = req.start_date or datetime.now().strftime("%Y-%m-%d")
    return {"success": True, "project_name": req.project_name, "start_date": start,
            "estimated_duration_days": days, "mode": "starter plan",
            "phases": [
                {"phase": "Pre-construction & approvals", "duration_days": 10, "status": "Planned"},
                {"phase": "Site preparation & foundation", "duration_days": max(8, req.floors*4), "status": "Planned"},
                {"phase": "Structure / frame", "duration_days": req.floors*10, "status": "Planned"},
                {"phase": "MEP and services", "duration_days": req.floors*5, "status": "Planned"},
                {"phase": "Finishes, inspection & handover", "duration_days": req.floors*7, "status": "Planned"}
            ],
            "reminders": ["Confirm permits and drawings before work starts.", "Track actual progress weekly.", "Add dependencies, resource loading, and local holidays before using this as a schedule."]}

@app.post("/api/assistant")
def assistant(req: TextRequest):
    q = req.message.lower()
    if any(w in q for w in ["concrete", "curing", "cement"]):
        answer = "For a demo checklist: verify the approved mix design, batching records, placement conditions, compaction, and curing plan. Follow the project specification and applicable code; do not use a generic chat answer as a substitute for the engineer's direction."
    elif any(w in q for w in ["crack", "裂"]):
        answer = "Document the crack location, width, length, date, and whether it changes. Cracks in columns, beams, slabs, or load-bearing elements should be assessed by a qualified structural engineer, especially if widening or accompanied by deflection or movement."
    elif any(w in q for w in ["safety", "helmet", "ppe"]):
        answer = "Start with a site-specific risk assessment, required PPE, edge protection, safe access, housekeeping, equipment inspection, and a clear incident-reporting route. Stop work and notify the safety lead if an immediate hazard is present."
    else:
        answer = "I can help structure a construction checklist, explain common terminology, or outline a planning workflow. Share the building type, stage, and applicable project specification for more relevant guidance. This demo does not replace qualified professional judgment."
    return {"success": True, "answer": answer, "mode": "demo assistant", "disclaimer": "Verify all safety, structural, and code-related decisions with qualified professionals."}

@app.post("/api/weather-advice")
def weather_advice(req: TextRequest):
    return {"success": True, "weather": {"condition": "Partly cloudy", "temperature_c": 29, "rain_chance_percent": 35, "source": "sample data"},
            "advice": ["Check an official local forecast before scheduling concrete pours or lifting operations.", "Protect cement and other moisture-sensitive materials.", "Reassess work-at-height and electrical risks during changing weather."],
            "mode": "demo; no live weather connection"}

@app.post("/api/knowledge")
def knowledge(req: TextRequest):
    return {"success": True, "topic": req.message,
            "answer": "Construction knowledge demo: define the issue, check the approved drawings and project specifications, confirm applicable local codes, document assumptions, and ask the responsible engineer or site manager to approve safety-critical decisions.",
            "mode": "demo knowledge base"}
