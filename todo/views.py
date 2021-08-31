import json
from todo.model_utils import FilterDictValidator
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden

from project.logger import Logger
from todo.models import Profile, Task
from .request_utils import (
    BadRequestException,
    withlogin,
    return_exception,
    NotFoundException,
    get_json_response,
    post_json_or_raise,
)


log = Logger.logger()


def check_if_online(request):
    return get_json_response()


@return_exception
def register(request):
    json_dictionary = post_json_or_raise(request)
    try:
        username = json_dictionary["username"]
        email = json_dictionary["email"]
        password = json_dictionary["password"]
    except KeyError:
        raise BadRequestException("Missing keys in json")
    user = User.objects.create_user(username, email, password)
    user.save()
    profile: Profile = Profile.objects.create(user=user, name="default")
    profile.save()
    profile.token = profile.generate_token()
    profile.save()
    return get_json_response(dictionary=profile.get_dict_repr())


@return_exception
def login(request):
    json_dictionary = post_json_or_raise(request)
    username = json_dictionary["username"]
    password = json_dictionary["password"]
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponseForbidden("Auth failed")
    profiles_query = Profile.objects.filter(user=user)
    result = {"profiles": []}
    for profile in profiles_query:
        result["profiles"].append({
            "name": profile.name,
            "token": profile.token
        })
    log.info(f"Successful login from {user.username}. Returning: {result}")
    return get_json_response(dictionary=result)


@withlogin
def check_token(request):
    log.info(f"User {request.user.id} ({request.user.username}) token valid")
    log.info(f"Request Profile: {request.profile}")
    dic = {
        "user": request.user.username,
        "profile": request.profile.name
    }
    return get_json_response(dictionary=dic)


@return_exception
@withlogin
def create_profile(request):
    json_dictionary = post_json_or_raise(request)
    profile_name = json_dictionary["name"]

    try:
        profile = Profile.objects.create(
            user=request.user,
            name=profile_name
        )
        profile.save()
        profile.token = profile.generate_token()
        profile.save()
        result = {
            "name": profile.name,
            "token": profile.token
        }
        return get_json_response(dictionary=result)
    except IntegrityError:
        error_dic = {
            "error": "User already has a profile with that name"
        }
        return get_json_response(status="conflict", dictionary=error_dic)


@return_exception
@withlogin
def rename_profile(request):
    json_dictionary = post_json_or_raise(request)
    try:
        old_name = json_dictionary["old_profile_name"]
        new_name = json_dictionary["new_profile_name"]
    except KeyError:
        raise BadRequestException("Missing old_name or new_name keys")
    profile = Profile.objects.filter(user=request.user, name=old_name).first()
    if profile is None:
        return NotFoundException("Could not find profile")
    try:
        profile.name = new_name
        profile.save()
    except IntegrityError:
        error_dic = {"error": "User already has a profile with that name"}
        return get_json_response(status="conflict", dictionary=error_dic)

    profile.token = profile.generate_token()
    profile.save()
    return get_json_response(dictionary=profile.get_dict_repr())


@return_exception
@withlogin
def delete_profile(request):
    json_dictionary = post_json_or_raise(request)
    try:
        profile_name = json_dictionary["profile_name"]
    except KeyError:
        raise BadRequestException("Missing profile_name")
    profile: Profile = Profile.objects.filter(
        user=request.user,
        name=profile_name
    ).first()
    if profile is not None:
        profile.delete()
    return get_json_response(dictionary={"deleted": True})


@return_exception
@withlogin
def add_task(request):
    task_dictionary = get_add_task_dictionary(request)
    task = Task.create_task(request.profile, task_dictionary)
    task.save()
    taskdic = task.get_dict_repr()
    log.info(f"Task {task.id} created for {request.profile}: {taskdic}")
    return get_json_response(dictionary=taskdic)


def get_add_task_dictionary(request) -> dict:
    jsondic: dict = post_json_or_raise(request)
    try:
        assert "title" in jsondic.keys()
        assert isinstance(jsondic["title"], str)
        assert len(jsondic["title"]) > 3
    except AssertionError:
        return BadRequestException("non empty title is required")
    return jsondic


@return_exception
@withlogin
def search_tasks(request):
    tasks = get_tasks_by_filter_dict(request.GET, request.profile)
    result = {
        "amount": len(tasks),
        "tasks": tasks
    }
    return get_json_response(dictionary=result)


def get_tasks_by_filter_dict(dictionary, profile):
    dict_validator = FilterDictValidator(dictionary)
    validated_dictionary = dict_validator.validate_search_dictionary()
    validated_dictionary["profile"] = profile
    log.info(f"Searching tasks with query {validated_dictionary}")
    queryset = Task.get_filtered_tasks(**validated_dictionary)
    tasks = []
    for task in queryset:
        tasks.append(task.get_dict_repr())
    return tasks


def get_valid_task_or_raise(request, task_id):
    task = Task.objects.filter(id=task_id).first()
    profile = request.profile
    if task is not None and task.profile == profile:
        return task
    raise NotFoundException(
        f"Could not find task {task_id} for profile {profile.id}"
    )


@return_exception
@withlogin
def done(request, task_id):
    task: Task = get_valid_task_or_raise(request, task_id)
    json_dictionary = post_json_or_raise(request)
    done = json_dictionary.get("done", None)
    if done is None:
        raise BadRequestException("missing param: done")
    task.done = done
    task.save()
    return get_json_response(dictionary=task.get_dict_repr())


@return_exception
@withlogin
def update_task(request, task_id):
    task: Task = get_valid_task_or_raise(request, task_id)
    json_dictionary = post_json_or_raise(request)
    dict_validator = FilterDictValidator(json_dictionary)
    valid_dic = dict_validator.validate_updateable_fields()
    Task.objects.filter(id=task.id).update(**valid_dic)
    task = Task.objects.get(id=task.id)
    return get_json_response(dictionary=task.get_dict_repr())


@return_exception
@withlogin
def delete_task(request, task_id):
    task: Task = get_valid_task_or_raise(request, task_id)
    task.delete()
    return get_json_response(dictionary={"deleted": True})


@return_exception
@withlogin
def task_children(request, task_id):
    task = get_valid_task_or_raise(request, task_id)
    filter_dictionary = request.GET.copy()
    filter_dictionary["parent_id"] = task.id
    filter_dictionary["search_sub_tree"] = True
    tasks = get_tasks_by_filter_dict(filter_dictionary, request.profile)
    return get_json_response(dictionary={"tasks": tasks})
