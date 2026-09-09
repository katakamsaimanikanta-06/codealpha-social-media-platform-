from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import Follow
from posts.models import Post, Like, Comment


class PostsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='author_user', password='password123', email='author@example.com')
        self.reader = User.objects.create_user(username='reader_user', password='password123', email='reader@example.com')
        self.stranger = User.objects.create_user(username='stranger_user', password='password123', email='stranger@example.com')

        self.post1 = Post.objects.create(author=self.author, content='Post by Author')
        self.post2 = Post.objects.create(author=self.stranger, content='Post by Stranger')

    def test_post_creation_view(self):
        self.client.login(username='author_user', password='password123')
        res = self.client.post(reverse('posts:feed'), {'content': 'My brand new post'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Post.objects.filter(content='My brand new post').exists())

    def test_post_edit_and_delete_permissions(self):
        # Reader cannot edit Author's post
        self.client.login(username='reader_user', password='password123')
        edit_url = reverse('posts:post_edit', args=[self.post1.id])
        res = self.client.post(edit_url, {'content': 'Hacked content'})
        self.assertEqual(res.status_code, 404)

        # Author can edit their post
        self.client.login(username='author_user', password='password123')
        res = self.client.post(edit_url, {'content': 'Updated content by author'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, 'Updated content by author')

        # Author can delete their post
        del_url = reverse('posts:post_delete', args=[self.post1.id])
        res = self.client.post(del_url, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Post.objects.filter(id=self.post1.id).exists())

    def test_like_toggle_api(self):
        self.client.login(username='reader_user', password='password123')
        like_url = reverse('posts:like_toggle', args=[self.post2.id])

        # Like
        res = self.client.post(like_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data['liked'])
        self.assertEqual(data['likes_count'], 1)

        # Unlike
        res = self.client.post(like_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertFalse(data['liked'])
        self.assertEqual(data['likes_count'], 0)

    def test_comment_creation_and_deletion(self):
        self.client.login(username='reader_user', password='password123')
        detail_url = reverse('posts:post_detail', args=[self.post2.id])

        # Add comment via AJAX
        res = self.client.post(detail_url, {'content': 'Great post stranger!'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['content'], 'Great post stranger!')
        self.assertEqual(self.post2.comments.count(), 1)

        # Delete comment
        comment = self.post2.comments.first()
        del_comment_url = reverse('posts:comment_delete', args=[comment.id])
        del_res = self.client.post(del_comment_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(del_res.status_code, 200)
        self.assertEqual(self.post2.comments.count(), 0)

    def test_following_feed_filtering(self):
        # Reader follows Author
        Follow.objects.create(follower=self.reader, following=self.author)

        self.client.login(username='reader_user', password='password123')

        # Following feed: should include Post by Author, but NOT Post by Stranger
        feed_res = self.client.get(reverse('posts:feed') + '?tab=following')
        self.assertEqual(feed_res.status_code, 200)
        self.assertContains(feed_res, 'Post by Author')
        self.assertNotContains(feed_res, 'Post by Stranger')

        # Explore feed: should include BOTH posts
        explore_res = self.client.get(reverse('posts:feed') + '?tab=explore')
        self.assertEqual(explore_res.status_code, 200)
        self.assertContains(explore_res, 'Post by Author')
        self.assertContains(explore_res, 'Post by Stranger')
