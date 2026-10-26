from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Booking, MenuItem
from .permissions import ReadOnlyOrTokenAuthenticated
from .serializers import BookingSerializer, MenuItemSerializer, RegistrationSerializer


def home(request):
    return render(request, "index.html")


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [ReadOnlyOrTokenAuthenticated]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("user").all()
    serializer_class = BookingSerializer
    permission_classes = [ReadOnlyOrTokenAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_id = response.data["id"]
        from django.contrib.auth import get_user_model
        user = get_user_model().objects.get(pk=user_id)
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"id": user.id, "username": user.username, "email": user.email, "token": token.key},
            status=201,
        )


class ObtainTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        from django.contrib.auth import authenticate
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request=request, username=username, password=password)
        if user is None:
            return Response({"detail": "Invalid username or password."}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
