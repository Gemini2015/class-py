#
#   Token Util
#
#   Copy from : https://github.com/jpulgarin/django-tokenapi
#

# coding=utf-8
from datetime import date
from django.utils.http import int_to_base36, base36_to_int
from django.utils import six
from django.utils.crypto import salted_hmac, constant_time_compare
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login


class TokenGenerator(object):
    """
    Util Class to make & check Token
    """
    def make_token(self, user):
        token = ""
        if settings.AUTH_TOKEN_ENABLE_TIMEOUT:
            token = self._make_token_with_timestamp(user, self._num_days(self._today()))
        else:
            token = self._make_token(user)

        return token


    def check_token(self, user, token):
        if settings.AUTH_TOKEN_ENABLE_TIMEOUT:
            return self._check_token_with_timestamp(user, token)
        else:
            return self._check_token(user, token)


    def _make_token_with_timestamp(self, user, timestamp):
        time_b36 = int_to_base36(timestamp)
        salt = 'ChrisCheng.Classmates'
        value = (six.text_type(user.pk) + user.password + six.text_type(time_b36))
        hash = salted_hmac(salt, value).hexdigest()[::2]
        return "%s-%s" % (time_b36, hash)


    def _check_token_with_timestamp(self, user, token):
        try:
            time_b36, hash = token.split('-')
        except ValueError:
            return False

        try:
            ts = base36_to_int(time_b36)
        except ValueError:
            return False

        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return False

        if (self._num_days(self._today()) - ts) > settings.AUTH_TOKEN_TIMEOUT_DAYS:
            return False

        return True


    def _make_token(self, user):
        salt = 'ChrisCheng.Classmates'
        value = (six.text_type(user.pk) + user.password)
        hash = salted_hmac(salt, value).hexdigest()[::2]

        return "%s" % hash


    def _check_token(self, user, token):
        if not constant_time_compare(self._make_token(user), token):
            return False

        return True


    def _num_days(self, d):
        return (d - date(2001, 1, 1)).days


    def _today(self):
        return date.today()


token_generator = TokenGenerator()


class TokenBackend(ModelBackend):
    def authenticate(self, pk, token = None):
        try:
            user = User.objects.get(pk = pk)
        except User.DoesNotExist:
            return None

        if token_generator.check_token(user, token):
            return user

        return None


def token_required(view_func):
    """
    token authentication decorator
    :param view_func:
    :return:
    """

    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = None
        token = None
        basic_auth = request.META.get('HTTP_AUTHORIZATION')

        if basic_auth:
            auth_method, auth_string = basic_auth.split(' ', 1)
            if auth_method.lower() == 'basic':
                auth_string = auth_string.strip().decode('base64')
                user, token = auth_string.split(':', 1)

        if not (user and token):
            user = request.POST.get('user')
            token = request.POST.get('token')

            if not user or not token:
                return HttpResponseForbidden('no user or token')

        if user and token:
            user = authenticate(pk = user, token = token)
            if user:
                login(request, user)
                return view_func(request, *args, **kwargs)

        return HttpResponseForbidden('auth failure')
    return _wrapped_view

