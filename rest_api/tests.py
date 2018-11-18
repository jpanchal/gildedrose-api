from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Itemlist
from django.contrib.auth.models import User


class ModelTestCase(TestCase):

    def setUp(self):
        user = User.objects.create(username="nerd")
        self.name = "Write world class code"
        self.itemlist = Itemlist(name=self.name, owner=user)

    def test_model_can_create_a_itemlist(self):
        """Test the itemlist model can create a itemlist."""
        old_count = Itemlist.objects.count()
        self.itemlist.save()
        new_count = Itemlist.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_returns_readable_representation(self):
        """Test a readable string is returned for the model instance."""
        self.assertEqual(str(self.itemlist), self.name)


class ViewsTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        # Since user model instance is not serializable, use its Id/PK
        self.itemlist_data = {'name': 'pillows', 'owner': user.id}
        self.response = self.client.post(
            reverse('create'),
            self.itemlist_data,
            format="json")

    def test_api_can_create_a_itemlist(self):
        """Test the api has item creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/itemlists/', kwargs={'pk': 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_can_get_a_itemlist(self):
        """Test the api can get a given itemlist."""
        itemlist = Itemlist.objects.get(id=1)
        response = self.client.get(
            '/itemlists/',
            kwargs={'pk': itemlist.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, itemlist)

    def test_api_can_update_itemlist(self):
        """Test the api can update a given itemlist."""
        itemlist = Itemlist.objects.get()
        change_itemlist = {'name': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': itemlist.id}),
            change_itemlist, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_itemlist(self):
        """Test the api can delete a itemlist."""
        itemlist = Itemlist.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': itemlist.id}),
            format='json',
            follow=True)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
