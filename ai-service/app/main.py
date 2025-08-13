from fastapi import FastAPI;
from app.api.analysis import router as analysis_router;

app = FastAPI(title="AI Service");
app.include_router(analysis_router);

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}