from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', null=True)
    like = models.ManyToManyField(User, related_name='like')
    created_date = models.DateField(auto_now_add=True)

    @property
    def comment(self):
        return self.comments_set.all()
    @property
    def likes(self):
        return self.like.all().count()

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_date = models.DateField(auto_now_add=True)
