from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GetEmpStatusInputSerializer, EmployeeStatusSerializer
from .services import DataAccess, Validator, ProcessStatus

class GetEmpStatusAPIView(APIView):
    """
    POST /api/GetEmpStatus
    payload: {"NationalNumber": "NAT1001"}
    """

    def post(self, request, *args, **kwargs):
        input_ser = GetEmpStatusInputSerializer(data=request.data)
        if not input_ser.is_valid():
            return Response({"error": "Invalid input", "details": input_ser.errors}, status=status.HTTP_400_BAD_REQUEST)

        data_access = DataAccess()
        validator = Validator()
        proc = ProcessStatus(data_access, validator)

        result, code = proc.compute(input_ser.validated_data)
        if code != 200:
            return Response(result, status=code)

        out_ser = EmployeeStatusSerializer(result)
        return Response(out_ser.data, status=status.HTTP_200_OK)
