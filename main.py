from typing import Union
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker
import db
import datetime

# new session
Session = sessionmaker(bind=db.engine)
session = Session()


app = FastAPI()


def create_user(session, user_id, first_name, last_name):
    user = db.User(user_id, first_name, last_name)
    session.add(user)
    # save changes to the database
    session.commit()


def create_loan(session, loan_id, user_id, amount, term, interest_rate):
    loan = db.Loan(loan_id, user_id, amount, term, interest_rate, datetime.datetime.now())
    session.add(loan)
    # save changes to the database
    session.commit()

def fetch_user(session)

# create_user(session, 2, 'adil', 'mezghouti')
create_loan(session, 1, 1, 300_000, 30, 0.06)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}