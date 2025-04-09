from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.users.serializers import UserRegisterSerializer, UserUpdateSerializer, UserDetailsSerializer


class RegisterViewSet(ViewSet):
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserRegisterSerializer,
        summary='Register a new user',
        description='Create a new user account',
        responses={
            201: UserRegisterSerializer,
            400: 'Bad Request',
        },
    )
    def create(self, request):  # Changed from post to create
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


class UserProfileViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get user profile',
        description='Get the profile of the currently authenticated user',
        responses={
            200: UserDetailsSerializer,
            401: 'Unauthorized',
        },
    )
    def list(self, request):
        user = request.user
        serializer = UserDetailsSerializer(user)
        return Response(serializer.data)

    @extend_schema(
        request=UserUpdateSerializer,
        summary='Update user profile',
        description='Update the profile of the currently authenticated user',
        responses={
            200: UserUpdateSerializer,
            400: 'Bad Request',
        },
    )
    @action(detail=False, methods=['patch'])
    def patch(self, request, pk=None):
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Delete user profile',
        description='Delete the profile of the currently authenticated user',
        responses={
            204: 'No Content',
            401: 'Unauthorized',
        },
    )
    @action(detail=False, methods=['delete'])
    def delete(self, request, pk=None):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
