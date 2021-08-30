import jwt
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100, blank=True, null=True)

    def generate_token(self):
        dic = {"id": self.id, "name": self.name, "user": self.user.username}
        secret = getattr(settings, "SECRET_TOKEN_KEY")
        token = jwt.encode(dic, secret, algorithm="HS256")
        return token

    @classmethod
    def get_profile(cls, token):
        try:
            secret = getattr(settings, "SECRET_TOKEN_KEY")
            dic = jwt.decode(token, secret, algorithms=["HS256"])
            profile = cls.objects.get(id=dic["id"])
            assert profile.name == dic["name"]
            assert profile.user.username == dic["user"]
            return profile
        except Exception:
            return None

    def __str__(self) -> str:
        return f"{self.user.username} / {self.name}"


# class Task(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     parent = models.ForeignKey('self', on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField(max_length=1000)
#     done = models.BooleanField(default=False)
