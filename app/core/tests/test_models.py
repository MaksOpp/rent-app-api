from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@gmail.com', password='password'):
    """Create a sample user"""
    return get_user_model().objects.create_user(
        email=email,
        password=password
    )


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = '12345678'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'mail@GMAIL.COM'
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@wp.pl',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Board Game'
        )

        self.assertEqual(str(tag), tag.name)

    def test_offer_str(self):
        """Test the offer string representation"""
        offer = models.Offer.objects.create(
            user=sample_user(),
            title='PS4',
            description='Nice console, great deal!',
            min_players=5,
            max_players=10,
            price_per_day=5.00,
            is_highlighted=False
        )

        self.assertEqual(str(offer), offer.title)
