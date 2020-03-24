import math
from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(issue__board=self).count()
        
    def get_issue_count(self):
        return Issue.objects.filter(board=self).count()

    def get_last_post(self):
        return Post.objects.filter(issue__board=self).order_by('-created_at').first()


class Issue(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField(max_length=4000)
    last_update = models.DateTimeField(auto_now=True)
    board = models.ForeignKey(Board, related_name='issues', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='issues', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def get_reply_count(self): 
        return Post.objects.filter(issue=self).count()-1
         
    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    issue = models.ForeignKey(Issue, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

  
