# model/orders.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

ordersRouter = APIRouter(tags=["Orders"])

# CRUD operations

@ordersRouter.get("/orders/", response_model=list)
async def read_orders(
    db=Depends(get_db)
):
    query = "SELECT OrderID, OrderStatus FROM orders"
    db[0].execute(query)
    orders = [{"OrderID": orders[0], "orderStatus": orders[1]} for orders in db[0].fetchall()]
    return orders


@ordersRouter.get("/orders/{OrderID}", response_model=dict)
async def read_orders(
    OrderID: int, 
    db=Depends(get_db)
):
    query = "SELECT OrderID, orderStatus FROM orders WHERE OrderID = %s"
    db[0].execute(query, (OrderID,))
    orders = db[0].fetchone()
    if orders:                             
        return {
            "OrderID": orders[0],
            "orderStatus": orders[1],
        }
    raise HTTPException(status_code=404, detail="Order not found")
