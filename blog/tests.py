from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment

class BlogTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create a test post
        self.post = Post.objects.create(
            title='Test Post Title',
            content='This is a test content for the blog post.',
            author=self.user
        )

    def test_post_list_view(self):
        """Test that the home feed loads successfully and displays posts"""
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post Title')
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_view(self):
        """Test that individual post detail pages render correctly"""
        response = self.client.get(reverse('post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This is a test content')

    def test_profile_access_unauthorized(self):
        """Test that unauthenticated users are redirected away from the profile page"""
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)
        # Should redirect to login
        self.assertRedirects(response, f"/login/?next=/profile/")

    def test_profile_access_authorized(self):
        """Test that authenticated users can access their profile page"""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')