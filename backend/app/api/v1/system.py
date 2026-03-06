from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["system"])

@router.get("/healthz", summary="Health check")
def healthz() -> dict[str, str]:
    return {"status": "ok"}