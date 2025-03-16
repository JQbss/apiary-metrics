from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers import UserRegisterSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserRegisterSerializer,
        summary='Register a new user',
        description='Create a new user account',
        responses={
            201: UserRegisterSerializer,
            400: 'Bad Request',
        },
    )
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            refresh_token = RefreshToken.for_user(serializer.instance)

            response_data = {
                'status': 'success',
                'message': 'User created successfully',
                'refresh_token': str(refresh_token),
                'access_token': str(refresh_token.access_token),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(
            {
                'status': 'error',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserRegisterSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserRegisterSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
