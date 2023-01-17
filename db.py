from sqlalchemy import func, and_, or_
from orm import Loan, LoanSchedule, User, Sharing
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
    return session.query(User).filter(User.email == email).all()


def fetch_loans(session, user_id):
    # Fetch the shared loans as well
    sharers = []
    for items in get_sharers(session, user_id):
        sharers.append(items[0])

    return session\
        .query(Loan.id,
               Loan.principal,
               Loan.interest_rate,
               Loan.term,
               Loan.created_at
               ) \
        .filter(or_(Loan.user_id == user_id, Loan.user_id.in_(sharers))) \
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
        func.coalesce(func.sum(LoanSchedule.interest_paid), 0),
        func.coalesce(func.sum(LoanSchedule.principal_paid), 0)
    ) \
        .filter(and_(LoanSchedule.loan_id == loan_id, LoanSchedule.month < month)) \
        .one()
    remaining_balance = session \
        .query(LoanSchedule.remaining_balance + LoanSchedule.principal_paid) \
        .filter(and_(LoanSchedule.loan_id == loan_id, LoanSchedule.month == month)) \
        .scalar()
    return interest_paid, principal_paid, remaining_balance


def share_loan(session, sharer_id, shared_with_id, loan_id):
    sharing = Sharing(sharer_id, shared_with_id, loan_id)
    session.add(sharing)
    session.flush()
    session.commit()
    return sharing


def get_sharers(session, shared_with_id):
    return session\
        .query(Sharing.sharer_id)\
        .filter(Sharing.shared_with_id == shared_with_id)\
        .all()


def user_exist(session, user_id):
    return session.query(func.count()).filter(User.id == user_id).scalar() > 0
