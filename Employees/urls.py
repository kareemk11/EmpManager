from django.urls import path
from .views import GetEmpStatusAPIView

urlpatterns = [
    path('GetEmpStatus/', GetEmpStatusAPIView.as_view(), name='get_emp_status'),
]
