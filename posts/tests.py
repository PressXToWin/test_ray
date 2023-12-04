from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_working_correctly(self):
        post = PostModelTest.post
        self.assertEqual(post.text, 'Тестовый пост')
        self.assertEqual(post.author, User.objects.get(username='auth'))
