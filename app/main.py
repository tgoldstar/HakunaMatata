from fastapi import FastAPI, Header, HTTPException, Depends
from app.routers import app_router, proj_router, poller_router
from app.auth import validate_key

app = FastAPI()

async def get_token_header(x_token: str = Header(...)):
    if not validate_key(x_token):
        raise HTTPException(status_code=400, detail="X-Token header invalid")

app.include_router(
    app_router.router,
    prefix="/app",
    tags=["app"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    proj_router.router,
    prefix="/proj",
    tags=["proj"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    poller_router.router,
    prefix="/poll",
    tags=["internal"],
    responses={404: {"description": "Not found"}},
)
@app.get('/')
def read_root():
    return {"Hello": "World"}
