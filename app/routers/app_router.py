from fastapi import APIRouter
from pydantic import BaseModel


class Remote(BaseModel):
    src: str
    user: str = None
    pw: str = None


class App(BaseModel):
    id: int = None
    name: str
    description: str = None
    remote: Remote
    port: int


router = APIRouter()


@router.put("/")
async def create_app(app: App):
    return app


@router.get("/{app_id}")
async def get_app(app_id: int):
    return


@router.get("/")
async def get_all_apps():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


@router.patch("/")
async def update_app():
    return


@router.delete("/")
async def delete_app():
    return
