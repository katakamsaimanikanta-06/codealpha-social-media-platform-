from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Profile, Follow


class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='userone', password='password123', email='userone@example.com')
        self.user2 = User.objects.create_user(username='usertwo', password='password123', email='usertwo@example.com')

    def test_profile_auto_created(self):
        self.assertTrue(hasattr(self.user1, 'profile'))
        self.assertEqual(self.user1.profile.followers_count, 0)
        self.assertEqual(self.user1.profile.following_count, 0)

    def test_follow_and_unfollow(self):
        # user1 follows user2
        follow = Follow.objects.create(follower=self.user1, following=self.user2)
        self.assertEqual(self.user2.profile.followers_count, 1)
        self.assertEqual(self.user1.profile.following_count, 1)

        # Unfollow
        follow.delete()
        self.assertEqual(self.user2.profile.followers_count, 0)
        self.assertEqual(self.user1.profile.following_count, 0)

    def test_cannot_follow_self(self):
        with self.assertRaises(Exception):
            Follow.objects.create(follower=self.user1, following=self.user1)

    def test_follow_toggle_view(self):
        self.client.login(username='userone', password='password123')
        url = reverse('accounts:follow_toggle', args=[self.user2.username])
        
        # Follow via AJAX
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['following'])
        self.assertEqual(data['followers_count'], 1)

        # Unfollow via AJAX
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['following'])
        self.assertEqual(data['followers_count'], 0)

    def test_registration_and_login(self):
        reg_url = reverse('accounts:register')
        reg_data = {
            'username': 'brandnewuser',
            'first_name': 'Brand',
            'last_name': 'New',
            'email': 'brandnew@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }
        res = self.client.post(reg_url, reg_data, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(User.objects.filter(username='brandnewuser').exists())

        # Logout
        self.client.get(reverse('accounts:logout'), follow=True)

        # Login
        login_res = self.client.post(reverse('accounts:login'), {'username': 'brandnewuser', 'password': 'password123'}, follow=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(login_res.context['user'].is_authenticated)
