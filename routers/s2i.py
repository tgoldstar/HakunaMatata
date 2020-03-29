from fastapi import APIRouter, HTTPException

router = APIRouter()


# C = Create
@router.put("/")
async def create_s2i():
    return 


# R = Read
@router.get("/")
async def read_items():
    return [{"name": "Item Foo"}, {"name": "item Bar"}]


# U = Update
@router.patch("/")
async def update_s2i():
    return


# D = Delete
@router.delete("/")
async def delete_s2i():
    return
