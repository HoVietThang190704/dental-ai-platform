from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
import time

router = FastAPI()

class AnalysisReq(BaseModel):
    image_url: HttpUrl | str
    options: dict | None = None

@router.post("/analyze")
async def analysis(req: AnalysisReq):
    t0 = time.time()
    return {
        "analysis_id": f"an_{int(t0)}",
        "findings": [
            {"tooth": 11, "issue": "caries", "severity": "mild", "confidence": 0.92}
        ],
        "overlay_url": "https://example.com/overlay.png",
        "duration_ms": int((time.time()-t0)*1000)
    }