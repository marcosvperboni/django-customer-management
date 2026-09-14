from django.contrib.auth.models import Group, Permission
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.models import User
from apps.accounts.serializers import (
    ChangePasswordSerializer,
    GroupSerializer,
    PermissionSerializer,
    RegisterSerializer,
    UserSerializer,
)
from apps.core.permissions import IsStaffOrReadOnly


class LoginView(TokenObtainPairView):
    pass


class RefreshView(TokenRefreshView):
    pass


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("email")
    serializer_class = UserSerializer
    permission_classes = [IsStaffOrReadOnly]
    filterset_fields = ["is_active", "is_staff"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["email", "date_joined"]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ["name"]


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all().order_by("content_type__model", "codename")
    serializer_class = PermissionSerializer
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ["name", "codename"]
