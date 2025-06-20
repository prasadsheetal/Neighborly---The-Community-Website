from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import BulletinItem

User = get_user_model()


class BulletinTests(APITestCase):

    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("token_obtain_pair")

        self.user_data = {
            "name": "Steve Harvey",
            "email": "steveharvey@example.com",
            "phone_number": "1234567890",
            "address": "123 Street, City",
            "city": "Test City",
            "zip_code": "12345",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "neighborhood": "Brooklyn",
            "account_type": "customer",
            "password": "password123",
        }

        self.token = self.authenticate_user()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.user = User.objects.get(email=self.user_data["email"])
        self.user_id = User.objects.get(email=self.user_data["email"]).id

    def authenticate_user(self):
        register_response = self.client.post(
            self.register_url, self.user_data, format="json"
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_response = self.client.post(
            self.login_url,
            {"email": self.user_data["email"], "password": self.user_data["password"]},
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", login_response.data)
        return login_response.data["access"]

    """==============Creation of bulletin=============="""

    def test_user_can_create_bulletin_item(self):
        payload = {
            "user_id": str(self.user_id),  # ADD this
            "title": "Community BBQ",
            "content": "Join us for a fun BBQ party this weekend!",
            "post_type": "event",
            "visibility": "public",
            "tags": ["BBQ", "Community", "Food"],
            "location": "Brooklyn",
            "city": "New York",
            "state": "NY",
            "zip_code": "11201",
            "neighborhood": "Brooklyn Heights",
        }

        url = "/bulletin/"
        response = self.client.post(url, data=payload, format="json")
        # Debugging print statement removed for cleaner test output

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BulletinItem.objects.count(), 1)

        bulletin = BulletinItem.objects.first()
        self.assertEqual(bulletin.title, "Community BBQ")
        self.assertEqual(bulletin.city, "New York")
        self.assertEqual(bulletin.visibility, "public")

        print("\n√ test_user_can_create_bulletin_item passed!")

    """==============Get Bulletin Details=============="""

    def test_get_bulletin_by_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        # Create bulletin using POST (not manual create)
        payload = {
            "user": self.user_id,
            "title": "Lost Cat",
            "content": "Please help find my missing cat, last seen near the park.",
            "post_type": "announcement",
            "visibility": "public",
            "tags": ["Lost", "Cat"],
            "location": "Brooklyn",
            "city": "New York",
            "state": "NY",
            "zip_code": "11201",
            "neighborhood": "Brooklyn Heights",
        }

        create_response = self.client.post("/bulletin/", data=payload, format="json")
        print(create_response)
        print("Create response:", create_response.content)

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        post_id = create_response.data["post_id"]

        # Now use the API to GET the bulletin
        url = f"/bulletin/{post_id}/"
        get_response = self.client.get(url)

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["title"], "Lost Cat")

        print("\n√ test_get_bulletin_by_id passed!")

    """==============Get Bulletin Details - invalid case=============="""

    def test_get_invalid_bulletin_returns_404(self):
        url = "/bulletin/invalid-id/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("\n√ test_get_invalid_bulletin_returns_404 passed!")

    """==============Get Bulletin List Requires Authentication=============="""

    def test_get_bulletin_requires_authentication(self):
        self.client.credentials()  # clear token
        response = self.client.get("/bulletin/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print("\n√ test_get_bulletin_requires_authentication passed!")

    """==============Filter Bulletins by Fields=============="""

    def test_filter_bulletins_by_city_and_tag(self):
        BulletinItem.objects.create(
            user=self.user,
            title="Art Workshop",
            content="Join our free art workshop this Saturday.",
            post_type="event",
            visibility="public",
            tags=["Art", "Workshop"],
            location="Manhattan",
            city="New York",
            state="NY",
            neighborhood="Chelsea",
        )

        BulletinItem.objects.create(
            user=self.user,
            title="Garage Sale",
            content="Selling household items.",
            post_type="announcement",
            visibility="public",
            tags=["Sale", "Garage"],
            location="Brooklyn",
            city="New York",
            state="NY",
            neighborhood="Williamsburg",
        )

        # Filter by city=New York and title containing "Art"
        response = self.client.get("/bulletin/?city=New York&title=Art&user=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Art Workshop")
        self.assertEqual(results[0]["city"], "New York")

        print("\n√ test_filter_bulletins_by_city_and_tag passed!")

    def test_get_user_bulletin_posts(self):
        # Create a second user
        other_user = User.objects.create_user(
            email="otheruser@example.com",
            password="otherpassword123",
            name="Other User",
            phone_number="0987654321",
            address="456 Other St, City",
            city="Other City",
            zip_code="54321",
            neighborhood="Other Neighborhood",
            account_type="customer",
        )

        # Create bulletins for the first (authenticated) user
        BulletinItem.objects.create(
            user=self.user,
            title="Post 1",
            content="Content 1",
            post_type="announcement",
            visibility="public",
            location="Location 1",
        )
        BulletinItem.objects.create(
            user=self.user,
            title="Post 2",
            content="Content 2",
            post_type="event",
            visibility="public",
            location="Location 2",
        )

        # Create a bulletin for the other user
        BulletinItem.objects.create(
            user=other_user,
            title="Other User Post",
            content="Other content",
            post_type="announcement",
            visibility="public",
            location="Other Location",
        )

        # Hit the endpoint for the first user's posts
        url = f"/bulletin/user/{self.user.user_id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = [post["title"] for post in response.data]
        self.assertIn("Post 1", titles)
        self.assertIn("Post 2", titles)

        print("\n√ test_get_user_bulletin_posts passed!")
