from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# connect to the database
engine = create_engine('sqlite:///loans.sqlite', echo=True)
# manage tables
base = declarative_base()


# we need the following objects: user, loan
class User(base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name


class Loan(base):
    __tablename__ = 'loans'

    loan_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, foreign_key=True)
    amount = Column(Integer)
    interest_rate = Column(Integer)
    term = Column(Integer)
    created_at = Column(Date)

    def __init__(self, loan_id, user_id, amount, interest_rate, term, created_at):
        self.loan_id = loan_id
        self.user_id = user_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.term = term
        self.created_at = created_at


base.metadata.create_all(engine)
