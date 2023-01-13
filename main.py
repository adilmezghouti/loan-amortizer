from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from orm import engine
from db import create_user, create_loan, fetch_user, fetch_loans
from models import User, Loan

# new session
Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()


# create_user(session, 'adil', 'mezghouti')
# create_loan(session, 1, 1, 300_000, 30, 0.06)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/users/")
def write_user(user: User):
    return create_user(session, user.first_name, user.last_name)


@app.post("/users/{user_id}/loans")
def write_load(user_id: int, loan: Loan):
    return create_loan(session, user_id, loan.principal, loan.term, loan.interest_rate)

@app.get("/users")
def read_user(first_name: str, last_name: str):
    users = fetch_user(session, first_name, last_name)
    if len(users) == 0:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return {"user": users[0]}


@app.get("/users/{user_id}/loans")
def read_loans(user_id: int):
    loans = fetch_loans(session, user_id)
    return {"loans": loans}
