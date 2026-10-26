from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import BookingViewSet, MenuItemViewSet, ObtainTokenView, RegisterView

router = DefaultRouter()
router.register("menu", MenuItemViewSet, basename="menu")
router.register("bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/token/", ObtainTokenView.as_view(), name="obtain-token"),
]
