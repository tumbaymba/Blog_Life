from django.test import TestCase
from django.urls import reverse


# Create your tests here.

class UserTestCase(TestCase):
    def setUp(self):
        self.register_url = reverse('users:register')

    def test_register_view(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
