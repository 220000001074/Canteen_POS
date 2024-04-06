# model/orders.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt
import mysql.connector
from pydantic import BaseModel





OrderRouter = APIRouter()
OrderRouter = APIRouter(tags=["orders"])



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


# ---------------------------------------------POST-----------------

@ordersRouter.post("/order/", response_model=dict)
async def create_orders(
    order_id: int = Form(...), 
    OrderStatus: str = Form(...), 
    orderDate: str = Form(...),
    orderTime: str = Form(...),
    orderTotal: int = Form(...), 
    db=Depends(get_db)
):

    query = "INSERT INTO orders (OrderID, OrderStatus, orderDate, orderTime, orderTotal) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (order_id, OrderStatus, orderDate, orderTime, orderTotal))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"OrderID": order_id, 
            "orderStatus": OrderStatus,
            "orderDate": orderDate,
            "orderTime": orderTime,
            "orderTotal": orderTotal,     
            }






# -------------------PUT/UPDATE----------------------------------
@ordersRouter.put("/order/{order_id}", response_model=dict)
async def update_order(
    order_id: int,
    Orderstatus: str,
    orderDate: str,
    orderTime: str,
    db=Depends(get_db)
):

    # Update cashier information in the database 
    query = "UPDATE orders SET Orderstatus = %s, orderDate = %s, orderTime =%s  WHERE OrderID = %s"
    db[0].execute(query, (Orderstatus, orderDate, orderTime, order_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Order updated successfully"}
    
    # If no rows were affected, cashier not found
    raise HTTPException(status_code=404, detail="Order not found")



    # Code na gikan sa CASHIER na DELETE---------------------------------

@ordersRouter.delete("/orders/{order_id}", response_model=dict)
async def delete_order(
    order_id: int,
    db=Depends(get_db)
):
    # try:
        # Check if the cashier exists
        query_check_order = "SELECT OrderID FROM orders WHERE OrderID = %s"
        db[0].execute(query_check_order, (order_id,))
        existing_order = db[0].fetchone()

        if not existing_order:
            raise HTTPException(status_code=404, detail="Order not found")

        # Delete the cashier
        query_delete_order = "DELETE FROM orders WHERE OrderID = %s"
        db[0].execute(query_delete_order, (order_id,))
        db[1].commit()

        return {"message": "Order deleted successfully"}
