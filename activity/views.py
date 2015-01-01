# coding=utf-8
# Create your views here.
from django.template import loader, Context, TemplateDoesNotExist
from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainapp.models import CommonInfo
from django.utils.translation import ugettext as _
import time
import json

from activity.models import Activity, UserActivity, Comment


@login_required(login_url="/login")
def activity_main_view(request):
    user = request.user
    info = CommonInfo.objects.get(user=user)

    # 判断是否存在活动
    if 0 == Activity.objects.count():
        activity_new_view(request)

    # 存在活动
    activities = Activity.objects.all()
    activity = activities[0]
    participant_id_list = UserActivity.objects.filter(item=activity.id, is_participate=True).values_list('user')
    participant_info_list = CommonInfo.objects.filter(id__in=participant_id_list)
    comments = Comment.objects.filter(item=activity.id).order_by('-datetime')
    try:
        temp = loader.get_template('activity_main.html')
    except TemplateDoesNotExist:
        return render_to_response('404.html', context=RequestContext(request))
    context = Context({
        'activities': activities,
        'activity': activity,
        'participants': participant_info_list,
        'comments': comments,
        'user': user,
        'userinfo': info,
        'ACTIVITY_STATUS': Activity.ACTIVITY_STATUS,
    })

    return HttpResponse(temp.render(context))


@login_required(login_url="/login")
def activity_new_view(request):
    if request.method == 'GET':
        # 获取创建活动页面
        user = request.user
        info = CommonInfo.objects.get(user=user)
        activities = Activity.objects.all()
        # 创建页面
        try:
            temp = loader.get_template("activity_new.html")
        except TemplateDoesNotExist:
            return render_to_response('404.html', context=RequestContext(request))
        # new页面渲染参数
        context = RequestContext(request=request, dict_={
            'activities': activities,
            'user': user,
            'userinfo': info,
        })
        return HttpResponse(temp.render(context))

    if request.method == 'POST':
        # 提交创建活动表单
        title = request.POST.get('title', '')
        datetime = request.POST.get('datetime', '')
        location = request.POST.get('location', '')
        creator = request.POST.get('creator', 0)
        organizer = request.POST.get('organizer', 0)
        content = request.POST.get('content', '')

        if title == '' or datetime == '' or location == '' or creator == 0:
            # 返回参数错误提示
            temp = loader.get_template('runscript.html')
            alertstr = _('Parameter error')
            url = 'activity/new'
            context = Context({
                'alertstr': alertstr, 'url': url
            })
            return HttpResponse(temp.render(context))

        activity = Activity()
        activity.title = title
        activity.datetime = datetime
        activity.location = location
        activity.creator = CommonInfo.objects.get(id=creator)
        if organizer == 0:
            activity.organizer = None
        else:
            activity.organizer = CommonInfo.objects.get(id=organizer)
        activity.content = content
        # Discussing
        activity.status = 1
        activity.save()

        return activity_info_view(request, activity.id)


@login_required(login_url="/login")
def activity_info_view(request, activity_id):
    activity = Activity.objects.filter(id=activity_id)
    if activity.count() == 0:
        temp = loader.get_template('runscript.html')
        alertstr = _('Activity not exists')
        url = 'activity'
        context = Context({
            'alertstr': alertstr, 'url': url
        })
        return HttpResponse(temp.render(context))
    activity = activity[0]
    user = request.user
    info = CommonInfo.objects.get(user=user)
    activities = Activity.objects.all()
    participant_id_list = UserActivity.objects.filter(item=activity.id, is_participate=True).values_list('user')
    participant_info_list = CommonInfo.objects.filter(id__in=participant_id_list)

    comments = Comment.objects.filter(item=activity.id).order_by('-datetime')
    try:
        temp = loader.get_template('activity_main.html')
    except TemplateDoesNotExist:
        return render_to_response('404.html', context=RequestContext(request))
    context = RequestContext(request=request, dict_={
        'activities': activities,
        'participants': participant_info_list,
        'activity': activity,
        'comments': comments,
        'user': user,
        'userinfo': info,
        'ACTIVITY_STATUS': Activity.ACTIVITY_STATUS,
    })

    return HttpResponse(temp.render(context))


@login_required(login_url='/login')
def activity_join_view(request):
    if 'activityid' not in request.GET:
        return json_return(2)

    activityid = request.GET.get('activityid', 0)
    userinfo = CommonInfo.objects.get(user=request.user)
    useractivity = UserActivity.objects.filter(user=userinfo, section=1, item=activityid)
    if useractivity.count() != 0:
        return json_return(5)

    useractivity = UserActivity()
    useractivity.user = userinfo
    useractivity.section = 1
    useractivity.item = activityid
    useractivity.is_participate = True
    useractivity.save()

    data = {
        'id': userinfo.user.id,
        'name': userinfo.cname
    }

    return json_return(1, data=data)


@login_required(login_url='/login')
def activity_quit_view(request):
    if 'activityid' not in request.GET:
        return json_return(2)

    activityid = request.GET.get('activityid', 0)
    userinfo = CommonInfo.objects.get(user=request.user)
    useractivity = UserActivity.objects.filter(user=userinfo, section=1, item=activityid)
    if useractivity.count() == 0:
        return json_return(4)

    useractivity = useractivity[0]

    data = {'id': userinfo.user.id, }

    useractivity.delete()

    return json_return(1, data=data)


@login_required(login_url='/login')
def activity_del_comment_view(request):
    if not request.user.is_staff:
        return json_return(3)

    if 'commentid' not in request.GET:
        return json_return(2)

    commentid = request.GET.get('commentid', 0)
    comment = Comment.objects.filter(id=commentid)
    if comment.count() == 0:
        return json_return(4)

    comment = comment[0]

    data = {'commentid': comment.id, }

    comment.delete()

    return json_return(1, data=data)


@login_required(login_url='/login')
def activity_post_comment_view(request):
    if 'comment' not in request.GET:
        return json_return(2)

    if 'activityid' not in request.GET:
        return json_return(2)

    content = request.GET.get('comment', '')
    activityid = request.GET.get('activityid', 0)
    if content == '' or activityid == 0:
        return json_return(2)

    user = request.user
    userinfo = CommonInfo.objects.get(user=user)
    comment = Comment()
    comment.commentator = userinfo
    comment.content = content
    comment.section = 1
    comment.item = activityid
    comment.is_anonymous = False
    current = time.localtime(time.time())
    datetime = time.strftime('%Y-%m-%d %H:%M:%S', current)
    comment.datetime = datetime
    comment.save()

    datetime = time.strftime('%Y-%m-%d %H:%M', current)
    data = {
        'name': userinfo.cname,
        'datetime': datetime,
        'commentid': comment.id,
        'is_staff': user.is_staff,
        'content': comment.content,
    }

    return json_return(1, data=data)


def json_return(code, data=None):
    res = HttpResponse()
    res['Content-Type'] = "text/javascript"

    error_dict = {
        1: 'success',
        2: 'invalid parameter',
        3: 'permission denied',
        4: 'object not exists',
        5: 'object already exists',
    }

    message = error_dict[code]
    if not message:
        message = 'unknown error'

    if not data:
        data = {}
    data['status'] = code
    data['message'] = message

    res.write(json.JSONEncoder().encode(data))
    return res
