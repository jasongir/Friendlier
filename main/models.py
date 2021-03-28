from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True, blank=True)
    picture = models.ImageField(upload_to='', null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title + ", last updated " + str(self.updated_at)

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.id])

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    message = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title + " on post " + str(self.post)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"id":self.post.id})



# https://stackoverflow.com/questions/21871386/make-models-belong-to-users-in-django