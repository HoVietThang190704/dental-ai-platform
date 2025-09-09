from fastapi import APIRouter
from app.core.config import RAW_DIR, PROCESSED_DIR, SPLITS_DIR

router = APIRouter()

@router.get("/debug-data-paths")
async def debug_data_paths():
    return {
        "raw": str(RAW_DIR), "raw_exists": RAW_DIR.exists(),
        "processed": str(PROCESSED_DIR), "processed_exists": PROCESSED_DIR.exists(),
        "splits": str(SPLITS_DIR), "splits_exists": SPLITS_DIR.exists(),
    }
