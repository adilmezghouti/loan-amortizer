import numpy as np

# loan amortization formula
# Monthly Payment = (P * (Interest Rate / Term)) / (1 - (1 + Interest Rate / Term)^(-Term * 12))


def monthly_payment(principal, interest_rate, term):
    numerator = (principal * (interest_rate / 12))
    denominator = (1 - np.power(1 + (interest_rate / 12), -term * 12))
    return numerator / denominator


amount = monthly_payment(300_000, 0.06, 30)
print(amount)
