from datetime import timedelta
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, MenuItem

User = get_user_model()


class MenuApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = MenuItem.objects.create(title="Greek Salad", price=Decimal("12.50"), inventory=10)

    def test_menu_list_is_public(self):
        response = self.client.get("/api/menu/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Greek Salad")

    def test_menu_create_requires_authentication(self):
        response = self.client.post(
            "/api/menu/",
            {"title": "Bruschetta", "price": "8.00", "inventory": 5},
            format="json",
        )
        self.assertEqual(response.status_code, 401)

    def test_authenticated_user_can_create_menu_item(self):
        user = User.objects.create_user(username="chef", password="SafePass123!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(
            "/api/menu/",
            {"title": "Bruschetta", "price": "8.00", "inventory": 5},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MenuItem.objects.filter(title="Bruschetta").exists())


class BookingApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_booking_can_be_created_by_authenticated_user(self):
        user = User.objects.create_user(username="customer", password="SafePass123!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(
            "/api/bookings/",
            {
                "name": "Alex Morgan",
                "no_of_guests": 2,
                "booking_date": (timezone.now() + timedelta(days=1)).isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, user)

    def test_booking_rejects_zero_guests(self):
        user = User.objects.create_user(username="customer2", password="SafePass123!")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        response = self.client.post(
            "/api/bookings/",
            {
                "name": "Alex Morgan",
                "no_of_guests": 0,
                "booking_date": (timezone.now() + timedelta(days=1)).isoformat(),
            },
            format="json",
        )
        self.assertEqual(response.status_code, 400)


class HomePageTests(TestCase):
    def test_homepage_serves_html(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Little Lemon")
