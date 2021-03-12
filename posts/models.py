from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    hashtags = models.ManyToManyField("Hashtags", related_query_name='posts')

    class Meta:
        ordering = ('-pub_date',)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'post')


class Favourite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('author', 'post')


class Hashtags(models.Model):
    hashtag = models.CharField(max_length=20, null=False)
