from unittest import TestCase
import numpy
from utils import calculate_payment_schedule, calculate_monthly_payment


class UtilsTesting(TestCase):
    def test_calculate_monthly_payment(self):
        monthly_payment = calculate_monthly_payment(principal=300_000, interest_rate=0.06, term=360)
        self.assertTrue(monthly_payment == 1_798.65)

    def test_calculate_payment_schedule(self):
        schedule = calculate_payment_schedule(principal=300_000, interest_rate=0.06, term=360)
        (monthly_payment_first, interest_paid_first, principal_paid_first, remaining_balance_first) = schedule[0]
        (monthly_payment_last, interest_paid_last, principal_paid_last, remaining_balance_last) = schedule[359]
        self.assertTrue(interest_paid_first == 1_500 and principal_paid_first == 298.65 and remaining_balance_first == 29_9701.35)
        self.assertTrue(interest_paid_last == 8.96 and principal_paid_last == 1_789.69 and remaining_balance_last == 1.58)


if __name__ == '__main__':
    TestCase.main()
