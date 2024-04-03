# model/menu.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

menuRouter = APIRouter(tags=["Menu"])

# CRUD operations

@menuRouter.get("/menu/", response_model=list)
async def read_menu(
    db=Depends(get_db)
):
    query = "SELECT ItemID, menuItemName FROM menu"
    db[0].execute(query)
    menu = [{"ItemID": user[0], "menuItemName": user[1]} for user in db[0].fetchall()]
    return menu


@menuRouter.get("/menu/{ItemID}", response_model=dict)
async def read_menu(
    ItemID: int, 
    db=Depends(get_db)
):
    query = "SELECT ItemID, menuItemName FROM menu WHERE ItemID = %s"
    db[0].execute(query, (ItemID,))
    menu = db[0].fetchone()
    if menu:                             
        return {
            "ItemID": menu[0],
            "menuItemName": menu[1],
        }
    raise HTTPException(status_code=404, detail="Item not found")


