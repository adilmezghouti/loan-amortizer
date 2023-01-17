from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from orm import engine
from db import create_user, create_loan, fetch_user, fetch_loans, fetch_loan_schedule, fetch_loan_summary, share_loan, user_exist
from models import User, Loan, Sharing

Session = sessionmaker(bind=engine)
session = Session()
app = FastAPI()


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.post("/users/")
def write_user(user: User):
    """Creates a new user"""
    try:
        return create_user(session, user.email, user.first_name, user.last_name)
    except exc.IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="User already exists!")
    except exc.SQLAlchemyError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")


@app.post("/users/{user_id}/loans")
def write_loan(user_id: int, loan: Loan):
    """Creates a loan for a user along with the amortization schedule"""
    # TODO We don't need to check for this if we had authentication
    if not user_exist(session, user_id):
        raise HTTPException(status_code=404, detail="User does not exist")
    try:
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
    except exc.SQLAlchemyError:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")


@app.get("/users")
def read_user(email: str):
    """Fetches a user using an email address"""
    try:
        users = fetch_user(session, email)
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")

    if len(users) == 0:
        raise HTTPException(status_code=404, detail="User not found with the given Email")
    return {"user": users[0]}


@app.get("/users/{user_id}/loans")
def read_loans(user_id: int):
    """Fetches a loan using a loan id"""
    if not user_exist(session, user_id):
        raise HTTPException(status_code=404, detail="User does not exist")

    try:
        loans = fetch_loans(session, user_id)
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")
    if len(loans) == 0:
        raise HTTPException(status_code=404, detail="Loan not found for the given user id")
    return {"loans": loans}


@app.get("/loans/{loan_id}/schedule")
def read_schedule(loan_id: int):
    """Fetches a loan schedule using a loan id"""
    try:
        schedule = fetch_loan_schedule(session, loan_id)
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")

    if len(schedule) == 0:
        raise HTTPException(status_code=404, detail="Schedule not found with the given loan id")
    return schedule


@app.get("/loans/{loan_id}/schedule/{month}")
def read_schedule_summary_for_month(loan_id: int, month: int):
    """Generates a loan schedule summary for the given month and loan id"""
    try:
        (interest_paid, principal_paid, remaining_balance) = fetch_loan_summary(session, loan_id, month)
        return {
            "principle_balance": remaining_balance,
            "principle_paid": principal_paid,
            "interest_paid": interest_paid
        }
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")


@app.post("/loans/{loan_id}/share")
def write_share_loan(loan_id: int, sharing: Sharing):
    """Shares a loan with another user"""
    if not user_exist(session, sharing.sharer_id) or not user_exist(session, sharing.shared_with_id):
        raise HTTPException(status_code=404, detail="One or both users don't exist!")
    try:
        result = share_loan(session, sharing.sharer_id, sharing.shared_with_id, loan_id)
        return {
            "id": result.id,
            "sharer_id": result.sharer_id,
            "shared_with_id": result.shared_with_id,
            "loan_id": result.loan_id,
            "created_at": result.created_at
        }
    except exc.SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error occurred. Please try again!")
