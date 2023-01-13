import numpy as np

# loan amortization formula
# Monthly Payment = (P * (Interest Rate / Term)) / (1 - (1 + Interest Rate / Term)^(-Term * 12))

# Term: number of months
def calculate_monthly_payment(principal, interest_rate, term):
    numerator = (principal * (interest_rate / 12))
    denominator = (1 - np.power(1 + (interest_rate / 12), -term))
    return numerator / denominator


def calculate_payment_schedule(principal, interest_rate, term):
    schedule_array = []
    monthly_rate = interest_rate/12
    monthly_payment = calculate_monthly_payment(principal, interest_rate, term)

    for i in range(term):
        interest_paid = monthly_rate * principal
        principal_paid = monthly_payment - interest_paid
        principal -= principal_paid
        schedule_array.append((monthly_payment, interest_paid, principal_paid, principal))

    return schedule_array


# monthly_payment = calculate_monthly_payment(100_000, 0.039, 360)
# monthly_payment = calculate_monthly_payment(300_000, 0.06, 360)
# print(monthly_payment)
# schedule = calculate_payment_schedule(300_000, 0.06, 360)
# print(schedule)
