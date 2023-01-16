from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
from orm import engine
from db import create_user, create_loan, fetch_user, fetch_loans, fetch_loan_schedule, fetch_loan_summary
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
    return create_user(session, user.email, user.first_name, user.last_name)


@app.post("/users/{user_id}/loans")
def write_loan(user_id: int, loan: Loan):
    (loan_id, principal, interest_rate, term) = create_loan(
        session,
        user_id,
        loan.principal,
        loan.term,
        loan.interest_rate
    )
    return {
        "id": loan_id,
        "principal": principal,
        "interest_rate": interest_rate,
        "term": term
    }
    # try:
    #     return create_loan(session, user_id, loan.principal, loan.term, loan.interest_rate)
    # except:
    #     raise HTTPException(status_code=404, detail="Failed to create a loan")


@app.get("/users")
def read_user(email: str):
    users = fetch_user(session, email)
    if len(users) == 0:
        raise HTTPException(status_code=500, detail="Item not found with the given ID")
    return {"user": users[0]}


@app.get("/users/{user_id}/loans")
def read_loans(user_id: int):
    loans = fetch_loans(session, user_id)
    return {"loans": loans}


@app.get("/loans/{loan_id}/schedule")
def read_schedule(loan_id: int):
    schedule = fetch_loan_schedule(session, loan_id)
    return schedule


@app.get("/loans/{loan_id}/schedule/{month}")
def read_schedule_summary_for_month(loan_id: int, month: int):
    (interest_paid, principal_paid, remaining_balance) = fetch_loan_summary(session, loan_id, month)
    return {
        "principle_balance": remaining_balance,
        "principle_paid": principal_paid,
        "interest_paid": interest_paid
    }

