from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/", include_in_schema=False)
def private():
    return
