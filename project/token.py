from django.http.response import HttpResponseBadRequest

from project.logger import Logger
from todo.models import Profile


log = Logger.logger()


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', b'').split()
        log.info(f"AUTH: {auth_header}")

        if auth_header and auth_header[0].lower() == 'token':
            if len(auth_header) != 2:
                return HttpResponseBadRequest("Improperly formatted token")

            profile = Profile.get_profile(auth_header[1])
            if profile is not None:
                request.profile = profile
                request.user = profile.user
        return self.get_response(request)
