from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


class App(BaseModel):
    name: str
    description: str
    source: str
    port: int
    
router = APIRouter()


@router.put("/")
async def create_app(app: App):
    return app


@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.patch("/")
async def update_s2i():
    return


@router.delete("/")
async def delete_app():
    return
