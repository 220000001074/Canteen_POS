# model/cashier.py
from asyncio.log import logger
from fastapi import Depends, HTTPException, APIRouter, Form
from .db import get_db
import bcrypt
from typing import Optional
from pydantic import BaseModel
import mysql.connector
class CashierCreate(BaseModel):
    username: str
    password: str

cashierRouter = APIRouter(tags=["Cashier"]) 

# CRUD operation

@cashierRouter.get("/cashier/", response_model=list)
async def read_cashier(
    db=Depends(get_db)
):
    query = "SELECT CashierID, username FROM cashier"
    db[0].execute(query)
    cashier = [{"CashierID": user[0], "username": user[1]} for user in db[0].fetchall()]
    return cashier


@cashierRouter.get("/cashier/{CashierID}", response_model=dict)
async def read_cashier(
    CashierID: int, 
    db=Depends(get_db)
):
    query = "SELECT CashierID, username FROM cashier WHERE CashierID = %s"
    db[0].execute(query, (CashierID,))
    cashier = db[0].fetchone()
    if cashier:                             
        return {
            "CashierID": cashier[0],
            "username": cashier[1],
        }
    raise HTTPException(status_code=404, detail="Cashier not found")




# --------------------POST---------------------------------------------------------------
@cashierRouter.post("/cashier/", response_model=CashierCreate)
async def create_cashier(cashier: CashierCreate, db=Depends(get_db)):
    try:
        # Construct the SQL query to insert a new cashier
        query = "INSERT INTO cashier (username, password) VALUES (%s, %s)"
        # Execute the query with the provided data
        db[0].execute(query, (cashier.username, cashier.password))
        # Commit the transaction
        db[1].commit()
        # Return the created cashier
        return cashier
    except Exception as e:
        # If an error occurs, raise an HTTPException with a 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the cursor and database connection
        db[0].close()



# -------------------------------PUT/UPDATE---------------------------------------------
@cashierRouter.put("/cashier/{cashierid}", response_model=dict)
async def update_cashier(
    cashierid: int,
    username: str,
    password: str,
    db=Depends(get_db)
):
    str_password = str(password)
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Update cashier information in the database 
    query = "UPDATE cashier SET username = %s, password = %s WHERE cashierID = %s"
    db[0].execute(query, (username, hashed_password, cashierid))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Cashier updated successfully"}
    
    # If no rows were affected, cashier not found
    raise HTTPException(status_code=404, detail="Cashier not found")



# -------------------DELETE------------------------------------------------------
@cashierRouter.delete("/cashier/{cashier_id}")
async def delete_cashier(cashier_id: int, 
                        db=Depends(get_db)):
    try:
        # Check if the cashier exists
        query_check_cashier = "SELECT cashierID FROM cashier WHERE cashierID = %s"
        db[0].execute(query_check_cashier, (cashier_id,))
        existing_cashier = db[0].fetchone()

        # If the cashier does not exist, raise HTTPException with 404 status code
        if not existing_cashier:
            raise HTTPException(status_code=404, detail="Cashier not found")

        # Delete the cashier from the database
        query_delete_cashier = "DELETE FROM cashier WHERE cashierID = %s"
        db[0].execute(query_delete_cashier, (cashier_id,))
        db[1].commit()

        # Return success message
        return {"message": "Cashier deleted successfully"}
    except Exception as e:
        # If an error occurs, raise HTTPException with 500 status code
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the cursor and database connection
        db[0].close()


