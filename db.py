import datetime
import orm
import utils


def create_user(session, first_name, last_name):
    user = orm.User(first_name, last_name)
    user.loans = []
    session.add(user)
    session.flush()
    session.commit()
    return user


def create_loan(session, user_id, principal, term, interest_rate):
    schedules = []
    user = fetch_user_by_id(session, user_id)
    print(user)
    # create the loan
    loan = orm.Loan(principal, term, interest_rate, datetime.datetime.now())

    # create the loan schedule
    for idx, record in enumerate(utils.calculate_payment_schedule(principal, interest_rate, term)):
        (monthly_payment, interest_paid, principal_paid, remaining_balance) = record
        schedules.append(orm.LoanSchedule(idx, monthly_payment, interest_paid, principal_paid, remaining_balance))

    loan.schedules = schedules
    loan.user_id = user_id
    # if hasattr(user, "loans"):
    #     user.loans.append(loan)
    # else:
    #     user.loans = [loan]
    session.add(loan)
    session.flush()
    session.commit()
    return loan


def fetch_user_by_id(session, user_id):
    return session.query(orm.User).filter(orm.User.id == user_id).one()

def fetch_user(session, first_name, last_name):
    users = []
    for user in session.query(orm.User).filter(orm.User.first_name == first_name and orm.User.last_name == last_name):
        users.append(user)

    return users

def fetch_loan_schedule(session):
    print()


def fetch_loan_summary(session, month):
    print(month)


def fetch_loans(session, user_id):
    print(user_id)


def share_loan(session, user_id_1, user_id_2):
    print(user_id_1, user_id_2)