from sqlalchemy import func, and_
from orm import Loan, LoanSchedule, User
import utils


def create_user(session, email, first_name, last_name):
    user = User(email, first_name, last_name)
    user.loans = []
    session.add(user)
    session.flush()
    session.commit()
    return user


def create_loan(session, user_id, principal, term, interest_rate):
    loan = Loan(user_id, principal, interest_rate, term)
    session.add(loan)
    session.flush()

    # create the loan schedule
    for idx, record in enumerate(utils.calculate_payment_schedule(principal, interest_rate, term)):
        (monthly_payment, interest_paid, principal_paid, remaining_balance) = record
        session.add(
            LoanSchedule(loan.id, idx + 1, monthly_payment, interest_paid, principal_paid, remaining_balance))

    session.commit()
    return loan.id, loan.principal, loan.interest_rate, loan.term


def fetch_user_by_id(session, user_id):
    return session.query(User).filter(User.id == user_id).one()


def fetch_user(session, email):
    return session.query(User).filter(User.email == email)


def fetch_loans(session, user_id):
    return session\
        .query(Loan.id,
               Loan.principal,
               Loan.interest_rate,
               Loan.term,
               Loan.created_at
               ) \
        .filter(Loan.user_id == user_id) \
        .all()


def fetch_loan_schedule(session, loan_id):
    return session \
        .query(LoanSchedule.month,
               LoanSchedule.remaining_balance,
               LoanSchedule.monthly_payment
               ) \
        .filter(LoanSchedule.loan_id == loan_id) \
        .all()


def fetch_loan_summary(session, loan_id, month):
    (interest_paid, principal_paid) = session \
        .query(
        func.sum(LoanSchedule.interest_paid),
        func.sum(LoanSchedule.principal_paid)
    ) \
        .filter(and_(LoanSchedule.loan_id == loan_id, LoanSchedule.month < month)) \
        .one()
    remaining_balance = session \
        .query(LoanSchedule.remaining_balance) \
        .filter(and_(LoanSchedule.loan_id == loan_id, LoanSchedule.month == month)) \
        .scalar()
    return interest_paid, principal_paid, remaining_balance


def share_loan(session, user_id_1, user_id_2):
    print(user_id_1, user_id_2)
