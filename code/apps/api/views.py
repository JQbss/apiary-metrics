from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorld(APIView):
    def get(self, request):
        return Response({"message": "Hello World from Apiary is API!asdasdasdads"},
                        status=status.HTTP_200_OK)
