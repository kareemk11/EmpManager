from rest_framework import serializers
from .models import User, Salary

class GetEmpStatusInputSerializer(serializers.Serializer):
    NationalNumber = serializers.CharField(max_length=50)


class EmployeeStatusSerializer(serializers.Serializer):
    EmployeeName = serializers.CharField()
    NationalNumber = serializers.CharField()
    HighestSalary = serializers.DecimalField(max_digits=12, decimal_places=2)
    AvarageSalary = serializers.DecimalField(max_digits=12, decimal_places=2)
    SumOfSalaries = serializers.DecimalField(max_digits=16, decimal_places=2)
    Status = serializers.CharField()
    IsActive = serializers.BooleanField()
    LastUpdated = serializers.DateTimeField()
