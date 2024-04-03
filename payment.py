# model/payment.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

paymentRouter = APIRouter(tags=["Payment"])

# CRUD operation

@paymentRouter.get("/payment/", response_model=list)
async def read_payment(
    db=Depends(get_db)
):
    query = "SELECT PaymentID, PaymentType FROM payment"
    db[0].execute(query)
    payment = [{"paymentID": payment[0], "paymentType": payment[0]} for payment in db[0].fetchall()]
    return payment



@paymentRouter.get("/payment/{PaymentID}", response_model=dict)
async def read_payment(
    PaymentID: int, 
    db=Depends(get_db)
):
    query = "SELECT PaymentID, PaymentType FROM payment WHERE PaymentID = %s"
    db[0].execute(query, (PaymentID,))
    payment = db[0].fetchone()
    if payment:                             
        return {"PaymentID": payment[0],
                "PaymentType": payment[1]}
    raise HTTPException(status_code=404, detail="Payment not found")
