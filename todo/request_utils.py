import json
from django.http.response import (
    HttpResponseNotFound,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    JsonResponse
)

from project.logger import Logger


log = Logger.logger()


def get_json_response(
    code=200,
    status="ok",
    dictionary=None
):
    json_dictionary = {
        "status": status,
    }
    if dictionary is not None:
        json_dictionary["result"] = dictionary
    return JsonResponse(json_dictionary, status=code)


def post_json_or_raise(request):
    try:
        return json.loads(request.body)
    except Exception:
        raise BadRequestException("Could not parse json")


class ForbiddenException(Exception):
    pass


class BadRequestException(Exception):
    pass


class NotFoundException(Exception):
    pass


def return_exception(func):
    def wraps(*args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except ForbiddenException as e:
            ret = HttpResponseForbidden(e.args[0])
            log.error(f"{ret} - {e.args[0]}")
        except NotFoundException as e:
            ret = HttpResponseNotFound(e.args[0])
            log.error(f"{ret} - {e.args[0]}")
        except BadRequestException as e:
            ret = HttpResponseBadRequest(e.args[0])
            log.error(f"{ret} - {e.args[0]}")
        return ret
    return wraps


def logged_in(func):
    def wraps(*args, **kwargs):
        try:
            assert args[0].user.is_authenticated
            ret = func(*args, **kwargs)
        except AssertionError:
            ret = HttpResponseForbidden("Missing Token")
        return ret
    return wraps
