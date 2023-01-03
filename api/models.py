from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField(upload_to='images',null=True)
    dateofbirth=models.DateField(null=True)
    place=models.CharField(max_length=100,null=True)
    bio=models.CharField(max_length=250 ,null=True)



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

    @property
    def imageURL(self):
        if self.image:
            return self.image.url
        else:
            return ""

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    created_date = models.DateField(auto_now_add=True)

class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    date = models.DateTimeField(auto_now_add=True)