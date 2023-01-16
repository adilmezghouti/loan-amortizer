from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# connect to the database
engine = create_engine('sqlite:///loans.sqlite', echo=True)

# manage tables
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    loans = relationship("Loan", back_populates="user")

    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return "<User (email=`%s`)>" % self.email


class Sharing(base):
    __tablename__ = 'sharing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sharer_id = Column(Integer, nullable=False)
    shared_with_id = Column(Integer, nullable=False)
    loan_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, sharer_id, shared_with_id, loan_id):
        self.sharer_id = sharer_id
        self.shared_with_id = shared_with_id
        self.loan_id = loan_id

class Loan(base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    principal = Column(Integer, nullable=False)
    interest_rate = Column(Integer, nullable=False)
    term = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="loans")
    schedule_records = relationship("LoanSchedule", back_populates="loan")

    def __init__(self, user_id, principal, interest_rate, term):
        self.user_id = user_id
        self.principal = principal
        self.interest_rate = interest_rate
        self.term = term

    def __repr__(self):
        return "<Loan (principal=`%f`)>" % self.principal


class LoanSchedule(base):
    __tablename__ = 'schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_id = Column(Integer, ForeignKey("loans.id"))
    month = Column(Integer, nullable=False)
    monthly_payment = Column(Float, nullable=False)
    interest_paid = Column(Float, nullable=False)
    principal_paid = Column(Float, nullable=False)
    remaining_balance = Column(Float, nullable=False)

    loan = relationship("Loan", back_populates="schedule_records")

    def __init__(self, loan_id, month, monthly_payment, interest_paid, principal_paid, remaining_balance):
        self.loan_id = loan_id
        self.month = month
        self.monthly_payment = monthly_payment
        self.interest_paid = interest_paid
        self.principal_paid = principal_paid
        self.remaining_balance = remaining_balance

    def __repr__(self):
        return "<LoanSchedule (remaining balance=`%f`)>" % self.remaining_balance


base.metadata.create_all(engine)
