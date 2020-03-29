from fastapi import FastAPI, Header, HTTPException, Depends
from .routers import s2i
from app.auth import validate_key

app = FastAPI()

async def get_token_header(x_token: str = Header(...)):
    if validate_key(x_token):
        raise HTTPException(status_code=400, detail="X-Token header invalid")

app.include_router(
    s2i.router,
    prefix="/s2i",
    tags=["s2i"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@app.get('/')
def read_root():
    return {"Hello": "World"}
