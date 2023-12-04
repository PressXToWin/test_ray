from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(verbose_name='Publication date', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    file = models.FileField(
        upload_to='posts/', null=True, blank=True)

    def __str__(self):
        return self.text
