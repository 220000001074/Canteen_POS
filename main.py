# main.py
from fastapi import FastAPI
from model.cashier import cashierRouter
from model.menu import menuRouter
from model.payment import paymentRouter
from model.orders import ordersRouter
from model.transaction import transactionRouter
from model.users import UsersRouter
from model.categories import CategoriesRouter
from model.expenses import ExpensesRouter

app = FastAPI()

# Include CRUD routes from modules
app.include_router(cashierRouter, prefix="/api")
app.include_router(menuRouter, prefix="/api")
app.include_router(ordersRouter, prefix="/api")
app.include_router(paymentRouter, prefix="/api")
app.include_router(transactionRouter, prefix="/api")
app.include_router(UsersRouter, prefix="/api")
app.include_router(CategoriesRouter, prefix="/api")
app.include_router(ExpensesRouter, prefix="/api")
