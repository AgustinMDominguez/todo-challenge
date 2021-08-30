import jwt
import json
from datetime import datetime

from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

from project.logger import Logger
from todo.model_utils import FilterDictValidator


log = Logger.logger()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    token = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('user', 'name')

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
        return f"{self.user.username}/{self.name}"


class Task(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    done = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self) -> str:
        return (
            f"{self.id} ({self.profile}) {self.title} "
            f"[{'X' if self.done else ' '}]"
        )

    def get_dict_repr(self):
        resultdic = json.loads(json.dumps(self.__dict__, default=str))
        resultdic.pop("_state", None)
        resultdic.pop("profile_id", None)
        return resultdic

    @classmethod
    def create_task(cls, profile: Profile, task_dict: dict):
        dict_validator = FilterDictValidator(task_dict)
        valid_dic = dict_validator.validate_updateable_fields()

        valid_dic["profile"] = profile

        if "parent_id" in valid_dic.keys():
            parent = cls.objects.filter(id=valid_dic["parent_id"]).first()
            if parent is not None and parent.profile == profile:
                valid_dic["parent"] = parent
                valid_dic.pop("parent_id")

        return cls.objects.create(**valid_dic)

    @classmethod
    def get_filtered_tasks(
        cls,
        profile: Profile,
        parent_id: int = None,
        title: str = None,
        tags: list = None,
        done: bool = None,
        start_time: datetime = None,
        end_time: datetime = None,
        page: int = 0,
        search_sub_tree: bool = False
    ) -> QuerySet:
        queryset = cls.objects.filter(profile=profile)
        if parent_id is not None:
            queryset = queryset.filter(parent__id=parent_id)
        elif not search_sub_tree:
            queryset = queryset.filter(parent__isnull=True)
        if title is not None:
            queryset = queryset.filter(title=title)
        if done is not None:
            queryset = queryset.filter(done=done)
        if tags is not None:
            queryset = cls.filter_by_tags(queryset, tags)
        if start_time is not None:
            queryset = queryset.filter(created_at__gt=start_time)
        if end_time is not None:
            queryset = queryset.filter(created_at__lt=end_time)
        return cls.get_queryset_page(queryset, page)

    @classmethod
    def filter_by_tags(cls, queryset: QuerySet, tags: list) -> QuerySet:
        return queryset

    @classmethod
    def get_queryset_page(cls, queryset: QuerySet, page: int) -> QuerySet:
        return queryset
