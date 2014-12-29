# coding=utf-8
from django.template import loader, Context, TemplateDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from mainapp.models import CommonInfo
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
import time
import json


# 登陆页面
def login_view(request):
    if request.user.is_authenticated():
        return main_view(request)

    if 'username' not in request.POST:
        try:
            temp = loader.get_template('signin.html')
            ctxdic = dict()
            if 'uid' in request.COOKIES:
                uid = request.COOKIES.get('uid', -1)
                users = User.objects.filter(id=uid)
                if users.exists():
                    user = users[0]
                    ctxdic['username'] = user.username
            context = RequestContext(request=request, dict_=ctxdic)
            return HttpResponse(temp.render(context))
        except TemplateDoesNotExist:
            return render_to_response('404.html', context_instance=RequestContext(request))

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        # 设置 session
        request.session['userid'] = user.id
        request.session.set_expiry(24 * 60 * 60)

        # 跳转到之前的页面
        nextpage = request.GET.get('next')
        if nextpage is None:
            nextpage = 'index'

        response = HttpResponseRedirect(nextpage)
        if 'rememberme' in request.POST and request.POST['rememberme'] == 'on':
            response.set_cookie('uid', user.id, max_age=24*60*60)
        return response

        #return main_view(request)
    else:
        temp = loader.get_template('runscript.html')
        alertstr = _('Account or password incorrect.')
        url = 'login'
        context = Context({
            'alertstr': alertstr, 'url': url
        })
        return HttpResponse(temp.render(context))



@login_required(login_url="/login")
def logout_view(request):
    auth.logout(request)
    return HttpResponseRedirect('login')


@login_required(login_url="/login")
def main_view(request):
    # 所有用户列表
    infolist = CommonInfo.objects.all()
    # 当前用户
    user = request.user
    # 当前用户信息
    #info = None
    try:
        info = CommonInfo.objects.get(user=user)
    except CommonInfo.DoesNotExist:
        # info未找到,新建一个信息
        info = CommonInfo(user=user)
        info.cname = "匿名的小伙伴"
        info.ename = ""
        info.birthday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        info.sex = ""
        info.bloodtype = ""
        info.cellphone = ""
        info.email = "xxxxx@xx.com"
        info.mailbox = ""
        info.homeaddr = ""
        info.currentaddr = "Mars"
        info.save()

    try:
        temp = loader.get_template("main.html")
    except TemplateDoesNotExist:
        return render_to_response('404.html', context=RequestContext(request))
    # main页面渲染参数
    context = Context({
        'infolist': infolist,
        'user': user,
        'userinfo': info,
        'info': info,
        'SEX_TYPE': CommonInfo.SEX_TYPE,
        'BLOOD_TYPE': CommonInfo.BLOOD_TYPE
    })

    return HttpResponse(temp.render(context))


@login_required(login_url="/login")
def info_view(request, userid):
    infolist = CommonInfo.objects.all()
    user = request.user
    userinfo = CommonInfo.objects.get(user=user)
    seluserqs = User.objects.filter(id=userid)

    # 如果选择的用户不存在，则弹出提示，然后跳转到main页面
    if not seluserqs.exists():
        temp = loader.get_template('runscript.html')
        alertstr = _('User you selected does not exists')
        url = 'index'
        context = Context({
            'alertstr': alertstr, 'url': url
        })
        return HttpResponse(temp.render(context))

    seluser = seluserqs[0]
    info = CommonInfo.objects.get(user=seluser)

    temp = loader.get_template("main.html")
    context = Context({
        'infolist': infolist,
        'user': user,
        'userinfo': userinfo,
        'info': info,
        'SEX_TYPE': CommonInfo.SEX_TYPE,
        'BLOOD_TYPE': CommonInfo.BLOOD_TYPE
    })

    return HttpResponse(temp.render(context))


@login_required(login_url="/login")
def editinfo_view(request, userid):
    # 如果当前用户不是Admin，或者与userid不符合，则弹出提示，然后跳转到main页面
    if request.user.id != long(userid) and (not request.user.is_staff):
        temp = loader.get_template('runscript.html')
        alertstr = _("Only staff can modify others' info")
        url = 'index'
        context = Context({
            'alertstr': alertstr, 'url': url
        })
        return HttpResponse(temp.render(context))

    seluserqs = User.objects.filter(id=userid)
    if not seluserqs.exists():
        return main_view(request)
    seluser = seluserqs[0]

    # 请求修改与修改提交使用同一个函数处理
    # 请求修改时 userid 会在GET里面
    # 修改提交时，数据在POST
    # 点击 Edit 按钮，会跳转到 main-edit 页面

    if 'userid' not in request.POST:
        infolist = CommonInfo.objects.all()
        user = request.user
        userinfo = CommonInfo.objects.get(user=user)
        info = CommonInfo.objects.get(user=seluser)

        return render_to_response('main-editinfo.html',
                                  {'infolist': infolist, 'user': user,
                                   'userinfo': userinfo, 'info': info,
                                   'SEX_TYPE': CommonInfo.SEX_TYPE, 'BLOOD_TYPE': CommonInfo.BLOOD_TYPE},
                                  context_instance=RequestContext(request))

    # 以下处理 修改提交
    info = CommonInfo.objects.get(user=seluser)
    # 超级管理员可以修改中文名
    if request.user.is_superuser:
        info.cname = request.POST.get('cname')
    info.ename = request.POST.get('ename')
    info.birthday = request.POST.get('birthday')
    info.sex = request.POST.get('sex')
    info.bloodtype = request.POST.get('bloodtype')
    info.cellphone = request.POST.get('cellphone')
    info.email = request.POST.get('email')
    info.mailbox = request.POST.get('mailbox')
    info.homeaddr = request.POST.get('homeaddr')
    info.currentaddr = request.POST.get('currentaddr')
    info.save()

    return info_view(request, userid)


@login_required(login_url="/login")
def password_view(request):
    user = request.user

    if 'oldpassword' not in request.POST:
        userinfo = CommonInfo.objects.get(user=user)
        return render_to_response('password.html', {'user': user, 'userinfo': userinfo},
                                  context_instance=RequestContext(request))

    oldpw = request.POST.get('oldpassword')
    newpw = request.POST.get('newpassword')
    comfirmpw = request.POST.get('confirmpassword')
    if newpw != comfirmpw:
        # js confirm newpw is equal to confirmpw
        url = 'password'
        alertstr = _('Password doesn\\\'t match the confirmation ')
        return render_to_response('runscript.html', Context({'alertstr': alertstr, 'url': url}))

    if user.check_password(raw_password=oldpw):
        user.set_password(raw_password=newpw)
        user.save()
        alertstr = _('Password change')
    else:
        alertstr = _('Raw password incorrect.')

    url = 'index'

    temp = loader.get_template('runscript.html')
    context = Context({
        'alertstr': alertstr, 'url': url
    })
    return HttpResponse(temp.render(context))


@login_required(login_url="/login")
def newuser_view(request):
    if not request.user.is_staff:
        return main_view(request)

    if 'username' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        newuserqs = User.objects.filter(username=username)
        if newuserqs.exists():
            alertstr = _('username exists.')
            temp = loader.get_template('runscript.html')
            url = 'index'
            context = Context({
                'alertstr': alertstr, 'url': url
            })
            return HttpResponse(temp.render(context))

        newuser = User.objects.create_user(username=username, password=password)
        newuser.is_active = True
        newuser.save()

        cname = request.POST.get('cname')
        info = CommonInfo(user=newuser)
        info.cname = cname
        info.ename = ""
        info.birthday = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        info.sex = ""
        info.bloodtype = ""
        info.cellphone = ""
        info.email = "xxxxx@xx.com"
        info.mailbox = ""
        info.homeaddr = ""
        info.currentaddr = "Mars"
        info.save()
        return main_view(request)

    user = request.user
    userinfo = CommonInfo.objects.get(user=user)

    return render_to_response('newuser.html', {'user': user, 'userinfo': userinfo},
                              context_instance=RequestContext(request))


@login_required(login_url="/login")
def deleteuser_view(request):
    tempuser = {}
    if 'userid' in request.GET:
        userid = request.GET.get('userid')

        deluserqs = User.objects.filter(id=userid)
        if deluserqs.exists() and not deluserqs[0].is_superuser:
            deluser = deluserqs[0]
            tempuser['id'] = deluser.id
            info = CommonInfo.objects.get(user=deluser)
            info.delete()
            # 实际上delete的默认行为为Cascade
            deluser.delete()

    #infolist = CommonInfo.objects.all()

    res = HttpResponse()
    res['Content-Type'] = "text/javascript"
    res.write(json.JSONEncoder().encode(tempuser))

    return res


