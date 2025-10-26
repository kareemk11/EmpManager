from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db import transaction
from django.db import DatabaseError
from django.conf import settings
from .models import User, Salary, ApiLog
import time

def quantize_dec(d):
    return d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class Validator:
    @staticmethod
    def validate_input(data):
        # data is expected to be validated by serializer already
        national = data.get("NationalNumber")
        if not national or not isinstance(national, str):
            raise ValueError("NationalNumber missing or invalid")
        # add extra format rules if needed
        return national.strip()


class DataAccess:
    """
    Encapsulates DB reads. Includes a retry mechanism for transient DB failures.
    """

    def __init__(self, max_retries=3, retry_sleep=0.5):
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep

    def _with_retry(self, func, *args, **kwargs):
        attempts = 0
        while True:
            try:
                return func(*args, **kwargs)
            except DatabaseError as e:
                attempts += 1
                ApiLog.objects.create(level="WARNING", message=f"DB error, attempt {attempts}", extra={"error": str(e)})
                if attempts >= self.max_retries:
                    raise
                time.sleep(self.retry_sleep)

    def get_user_by_national(self, national_number):
        return self._with_retry(lambda: User.objects.filter(national_number=national_number).first())

    def get_salaries_for_user(self, user):
        return self._with_retry(lambda: list(Salary.objects.filter(user=user).order_by('year', 'month')))


class ProcessStatus:
    """
    Orchestrates validation, data access and business logic computation.
    """

    SUM_TAX_THRESHOLD = Decimal('10000')
    TAX_RATE = Decimal('0.07')

    def __init__(self, data_access: DataAccess, validator: Validator):
        self.data_access = data_access
        self.validator = validator

    def compute(self, input_data):
        
        national = self.validator.validate_input(input_data)

        user = self.data_access.get_user_by_national(national)
        if not user:
            return {"error": "Invalid National Number"}, 404

        if not user.is_active:
            return {"error": "User is not Active"}, 406

        salaries = self.data_access.get_salaries_for_user(user)
        if len(salaries) < 3:
            return {"error": "INSUFFICIENT_DATA"}, 422

        adjusted = []
        for s in salaries:
            base = Decimal(s.salary)
            if s.month == 12:
                adj = base * Decimal('1.10')
            elif s.month in (6, 7, 8):
                adj = base * Decimal('0.95')
            else:
                adj = base
            adjusted.append(quantize_dec(adj))

        total_before_tax = sum(adjusted, Decimal('0.00'))
        total_after_tax = total_before_tax
        if total_before_tax > self.SUM_TAX_THRESHOLD:
            deduction = (total_before_tax * self.TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_after_tax = total_before_tax - deduction

        count = Decimal(len(adjusted))
        average_after_tax = (total_after_tax / count).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        highest_salary = max(adjusted)
        sum_of_salaries = quantize_dec(total_after_tax)  # sum after tax deduction applied (per spec)

        if average_after_tax > Decimal('2000'):
            status = "GREEN"
        elif average_after_tax == Decimal('2000'):
            status = "ORANGE"
        else:
            status = "RED"

        result = {
            "EmployeeName": user.username,
            "NationalNumber": user.national_number,
            "HighestSalary": quantize_dec(highest_salary),
            "AvarageSalary": average_after_tax,
            "SumOfSalaries": sum_of_salaries,
            "Status": status,
            "IsActive": user.is_active,
            "LastUpdated": timezone.now()
        }

        ApiLog.objects.create(level="INFO", message="GetEmpStatus computed", extra={
            "national_number": user.national_number,
            "count_salaries": len(salaries),
            "sum_before_tax": str(total_before_tax),
            "sum_after_tax": str(total_after_tax),
            "average_after_tax": str(average_after_tax),
        })

        return result, 200
