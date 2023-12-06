from django.test import TestCase
from rest_framework.test import APIClient, APITestCase

from posts.models import Post, User


class PostTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(author=cls.user, text="test text 1")

    def setUp(self):
        self.user = User.objects.get(username='auth')
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)

    def test_get_request_return_posts(self):
        posts = self.authorized_client.get('/api/v1/posts/', format='json')
        self.assertEqual(len(posts.data), 1, 'Проверьте, отдаёт ли GET-запрос список постов')

    def test_post_request_adds_post(self):
        new_post = self.authorized_client.post('/api/v1/posts/', data={'text': 'test text 2'}, format='json')
        self.assertEqual(new_post.data['text'], 'test text 2', 'Проверьте, создаёт ли POST-запрос новый пост')
        self.assertEqual(Post.objects.count(), 2, 'Проверьте, создаёт ли POST-запрос новый пост')
        self.assertEqual(new_post.data['author'], 'auth', ('Убедитесь, что при создании поста '
                                                           'указывается правильный пользователь'))

    def test_patch_request(self):
        self.authorized_client.patch('/api/v1/posts/1/', data={
            'text': 'test text 3'
        }, format='json')
        self.assertEqual(Post.objects.get(id=1).text, 'test text 3', 'Проверьте, изменяет ли PATCH-запрос пост')

    def test_put_request(self):
        self.authorized_client.put('/api/v1/posts/1/', data={
            'text': 'test text 4'
        }, format='json')
        self.assertEqual(Post.objects.get(id=1).text, 'test text 4', 'Проверьте, изменяет ли PUT-запрос пост')

    def test_delete_request(self):
        post_for_delete = self.authorized_client.delete('/api/v1/posts/1/', format='json')
        self.assertEqual(post_for_delete.status_code, 204, 'Убедитесь, что DELETE-запрос удаляет пост')
        self.assertEqual(Post.objects.count(), 0, 'Убедитесь, что DELETE-запрос удаляет пост')
