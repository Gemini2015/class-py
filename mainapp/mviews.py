__author__ = 'Gemini'
# coding=utf-8
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
import json
from mainapp.tokens import token_generator, token_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _


@csrf_exempt
def login_view(request):
    res = HttpResponse()
    res['Content-Type'] = "text/javascript"
    #ret.write(json.JSONEncoder().encode(tempuser))
    if 'username' not in request.POST or 'password' not in request.POST:
        ret = {
            'status': 0, # no username or password
        }
        res.write(json.JSONEncoder().encode(ret))
        return res

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username = username, password = password)
    if user:
        ret = {
            'status': 1, # login success
            'token': token_generator.make_token(user),
            'user': user.pk
        }
        res.write(json.JSONEncoder().encode(ret))
        return res
    else:
        ret = {
            'status': 2,  # username or password error
        }
        res.write(json.JSONEncoder().encode(ret))
        return res


@token_required
def get_info(request):
    res = HttpResponse()
    res['Content-Type'] = "text/javascript"
    ret = {
            'status': 1, # please re-login
    }
    res.write(json.JSONEncoder().encode(ret))
    return res