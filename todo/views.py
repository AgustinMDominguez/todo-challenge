from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from .utils import get_json_response, post_json_or_raise, return_exception
from project.logger import Logger


log = Logger.logger()


def checkOnline(request):
    return get_json_response()


@return_exception
def login(request):
    request_json = post_json_or_raise(request)
    username = request_json["username"]
    password = request_json["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        token = Token.objects.create(user=user)
        dictionary = {"logged_in": True, "token": token.key}
        log.info(f"User {user.id} ({user.username}) is now loggued in")
    else:
        dictionary = {"logged_in": False, "token": None}
    return get_json_response(dictionary=dictionary)


@login_required
def is_logged_in(request):
    log.info(request.auth)
    log.info(request.user)
    return get_json_response()

