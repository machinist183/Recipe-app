from django.contrib.auth import get_user_model
from django.test import TestCase , Client
from django.urls import reverse


class AdminTest(TestCase):

    def setUp(self):

        self.client = Client()
        self.adminUser = get_user_model().objects.create_superuser(
            email = 'admin1@example.com',
            password = 'adminpass123',
        )
        self.client.force_login(self.adminUser)

        self.testUser = get_user_model().objects.create_user(
            email = 'test1@example.com',
            password = 'test1pass123',
        )

    def test_user_is_visible_in_admin(self):

        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res , self.testUser.email)
        self.assertContains(res , self.testUser.first_name)

    def test_admin_user_change_page_available(self):

        url = reverse('admin:core_user_change' , args=[self.testUser.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code , 200)

    def test_admin_user_add_page(self):
        
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code , 200)

