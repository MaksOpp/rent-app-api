from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Offer

from offer.serializers import OfferSerializer


OFFERS_URL = reverse('offer:offer-list')


def sample_offer(user, **params):
    """Create and return a sample offer"""
    defaults = {
        'title': 'Sample offer',
        'description': 'Nice console, great deal!',
        'min_players': 2,
        'max_players': 6,
        'price_per_day': 5.00,
        'is_highlighted': False,
    }
    defaults.update(params)

    return Offer.objects.create(user=user, **defaults)


class PublicOfferApiTests(TestCase):
    """Test unauthenticated offer API access"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Test the authenticaiton is required"""
        res = self.client.get(OFFERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOfferApiTests(TestCase):
    """Test authenticated offer API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_offers(self):
        """Test retrieving list of offers"""
        sample_offer(user=self.user)
        sample_offer(user=self.user)

        res = self.client.get(OFFERS_URL)

        offers = Offer.objects.all().order_by('-id')
        serializer = OfferSerializer(offers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_offers_limited_to_user(self):
        """Test retrieving offers for user"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'password'
        )
        sample_offer(user=user2)
        sample_offer(user=self.user)

        res = self.client.get(OFFERS_URL)

        offers = Offer.objects.filter(user=self.user)
        serializer = OfferSerializer(offers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
