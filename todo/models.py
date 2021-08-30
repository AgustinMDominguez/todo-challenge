from django.db import models
from django.contrib.auth.models import User

# class Profile(model.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)


# class Task(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField(max_length=1000)
#     done = models.BooleanField(default=False)

