from fastapi import APIRouter
from pydantic import BaseModel


class Project(BaseModel):
    id: int = None
    name: str
    desc: str = None


router = APIRouter()


@router.put("/")
def create_proj(proj: Project):
    return proj


@router.get("/{proj_id}")
def get_proj(proj_id: int):
    return Project(id=1, name="HakunaMatata")


@router.get("/")
def get_all_proj():
    return Project(id=1, name="HakunaMatata", desc="That it all projects")


@router.patch("/{proj_id}")
def update_proj(proj_id: int, proj: Project):
    proj.id = proj_id
    return proj


@router.delete("/{proj_id}")
def delete_proj(proj_id: int):
    return proj_id
