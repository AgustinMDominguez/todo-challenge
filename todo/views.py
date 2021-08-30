from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http.response import HttpResponseForbidden

from project.logger import Logger
from todo.models import Profile
from .request_utils import (
    logged_in,
    return_exception,
    get_json_response,
    post_json_or_raise,
)


log = Logger.logger()


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


def create_profile(request):
    pass


def check_if_online(request):
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
    result = {"profiles":[]}
    for profile in profiles_query:
        result["profiles"].append({
            "name": profile.name,
            "token": profile.token
        })
    log.info(f"Successful login from {user.username}. Returning: {result}")
    return get_json_response(dictionary=result)


@logged_in
def is_logged_in(request):
    log.info(f"User {request.user.id} ({request.user.username}) is logged in")
    log.info(f"Request Profile: {request.profile}")
    dic = {
        "user": request.user.username,
        "profile": request.profile.name
    }
    return get_json_response(dictionary=dic)

