# model/transaction.py
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt

transactionRouter = APIRouter(tags=["Transaction"])

# CRUD operations

@transactionRouter.get("/transaction/", response_model=list)
async def read_transaction(
    db=Depends(get_db)
):
    query = "SELECT transactionID, Subtotal FROM transaction"
    db[0].execute(query)
    transaction = [{"transactionID": transaction[0], "Subtotal": transaction[1]} for transaction in db[0].fetchall()]
    return transaction


@transactionRouter.get("/transaction/{transactionID}", response_model=dict)
async def read_transaction_by_id(
    ItemID: int, 
    db=Depends(get_db)
):
    query = "SELECT transactionID, Subtotal FROM transaction WHERE transactionID = %s"
    db[0].execute(query, (ItemID,))
    transaction = db[0].fetchone()
    if transaction:                             
        return {
            "transactionID": transaction[0],
            "Subtotal": transaction[1],
        }
    raise HTTPException(status_code=404, detail="Transaction not found")
