from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)
    national_number = models.CharField(max_length=50, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.national_number})"


class Salary(models.Model):
    user = models.ForeignKey(User, related_name="salaries", on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()  
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ["year", "month"]

    def __str__(self):
        return f"{self.user.national_number} - {self.year}/{self.month}: {self.salary}"


class ApiLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20)
    message = models.TextField()
    extra = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"[{self.level}] {self.timestamp}: {self.message[:80]}"
