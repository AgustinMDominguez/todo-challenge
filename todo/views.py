import ast

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden

from project.logger import Logger
from todo.models import Profile, Task
from .request_utils import (
    BadRequestException,
    get_datetime,
    withlogin,
    return_exception,
    get_json_response,
    post_json_or_raise,
)


log = Logger.logger()


def check_if_online(request):
    return get_json_response()


@return_exception
def register(request):
    json_dictionary = post_json_or_raise(request)
    username = json_dictionary["username"]
    email = json_dictionary["email"]
    password = json_dictionary["password"]
    user = User.objects.create_user(username, email, password)
    user.save()
    profile = Profile.objects.create(user=user, name="default")
    profile.save()
    profile.token = profile.generate_token()
    profile.save()
    return get_json_response()


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


def create_profile(request):
    return get_json_response()


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
    validated_dictionary = get_validated_filter_task_dict(request.GET)
    validated_dictionary["profile"] = request.profile
    log.info(f"Searching tasks with query {validated_dictionary}")
    queryset = Task.get_filtered_tasks(**validated_dictionary)
    result = {"tasks": []}
    for task in queryset:
        result["tasks"].append(task.get_dict_repr())
    return get_json_response(dictionary=result)


def get_validated_filter_task_dict(reqdic: dict) -> dict:
    valid_dic = {}
    args_schema = {
        "parent_id": int,
        "title": str,
        "favorite": bool,
        "page": int,
        "search_sub_tree": bool,
        "done": bool,
    }

    tags = reqdic.get("tags", None)
    if tags is not None:
        try:
            assert isinstance(tags, list)
            for tag in tags:
                assert isinstance(tag, str)
            valid_dic["tags"] = tags
        except Exception as e:
            log.error(f"Tags '{tags}' are malformed. Error: {e}")

    for arg in args_schema:
        if arg in reqdic.keys():
            try:
                eval = ast.literal_eval(reqdic[arg])
                assert isinstance(eval, args_schema[arg])
                valid_dic[arg] = eval
            except Exception as e:
                log.error(e)
                log.error(f"argument {arg} is not {args_schema[arg]}")

    start_time = get_datetime(reqdic.get("start_time", None))
    if start_time is not None:
        valid_dic["start_time"] = start_time
    end_time = get_datetime(reqdic.get("end_time", None))
    if end_time is not None:
        valid_dic["end_time"] = end_time

    return valid_dic


@return_exception
@withlogin
def done(request, task_id):
    return get_json_response()


@return_exception
@withlogin
def update_task(request, task_id):
    return get_json_response()


@return_exception
@withlogin
def delete_task(request, task_id):
    return get_json_response()


@return_exception
@withlogin
def task_children(request, task_id):
    return get_json_response()
