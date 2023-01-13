from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey,create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# connect to the database
engine = create_engine('sqlite:///loans.sqlite', echo=True)

# manage tables
base = declarative_base()


# we need the following objects: user, loan
class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    loans = relationship("Loan", back_populates="user")

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "<User (first name=`%s`)>" % self.first_name


class Loan(base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    principal = Column(Integer)
    interest_rate = Column(Integer)
    term = Column(Integer)
    created_at = Column(Date)

    user = relationship("User", back_populates="loans")
    schedule_records = relationship("LoanSchedule", back_populates="loan")

    def __init__(self, principal, interest_rate, term, created_at):
        self.principal = principal
        self.interest_rate = interest_rate
        self.term = term
        self.created_at = created_at

    def __repr__(self):
        return "<Loan (principal=`%f`)>" % self.principal


class LoanSchedule(base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    month = Column(Integer)
    monthly_payment = Column(Float)
    interest_paid = Column(Float)
    principal_paid = Column(Float)
    remaining_balance = Column(Float)

    loan = relationship("Loan", back_populates="schedule_records")

    def __init__(self, month, monthly_payment, interest_paid, principal_paid, remaining_balance):
        self.month = month
        self.monthly_payment = monthly_payment
        self.interest_paid = interest_paid
        self.principal_paid = principal_paid
        self.remaining_balance = remaining_balance

    def __repr__(self):
        return "<LoanSchedule (remaining balance=`%f`)>" % self.remaining_balance


base.metadata.create_all(engine)
