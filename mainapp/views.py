from django.template import loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from mainapp.models import User, CommonInfo
from django.shortcuts import render, render_to_response, RequestContext
from django.core import serializers
import time
import hashlib

# Create your views here.

def login_view(request):
	if 'account' in request.POST:
		account = request.POST.get('account')
		password = request.POST.get('password')
		#md = hashlib.md5
		#value = md(password)
		#valuepw = value.hexdigest()

		user = User.objects.filter(account = account)
		if user and user[0].password == password:
			request.session['user_id'] = user[0].id
			return main_view(request)

	return render_to_response('signin.html', context_instance=RequestContext(request))

def logout_view(request):
	request.session.flush()
	return HttpResponseRedirect('login')

def main_view(request):
	if request.session.get('user_id', -1) == -1:
		return render_to_response('signin.html', context_instance=RequestContext(request))

	userList = User.objects.all()
	userId = request.session['user_id']
	currentUser = User.objects.get(id = userId)
	info = CommonInfo.objects.get(user_id = userId)

	temp = loader.get_template("main.html")
	context = Context({
		'userList': userList,
		'currentUser': currentUser, 
		'info': info
		})

	return HttpResponse(temp.render(context))

def info_view(request,userId):
	if request.session.get('user_id', -1) == -1:
		return render_to_response('signin.html', context_instance=RequestContext(request))

	userList = User.objects.all()
	currentUserId = request.session['user_id']
	currentUser = User.objects.get(id = currentUserId)
	infoqs = CommonInfo.objects.filter(user_id = userId)
	if infoqs:
		info = infoqs[0]
	else:
		info = CommonInfo.objects.get(user_id = currentUserId)

	temp = loader.get_template("main.html")
	context = Context({
		'userList': userList,
		'currentUser': currentUser, 
		'info': info
		})

	return HttpResponse(temp.render(context))	

def editinfo_view(request, userId):
	if request.session.get('user_id', -1) == -1:
		return render_to_response('signin.html', context_instance=RequestContext(request))

	userqs = User.objects.filter(id = userId)
	if not userqs:
		return main_view(request)

	if 'id' not in request.POST:
		#user = userqs[0]
		userList = User.objects.all()
		currentUserId = request.session['user_id']
		currentUser = User.objects.get(id = currentUserId)	
		infoqs = CommonInfo.objects.filter(user_id = userId)
		if infoqs:
			info = infoqs[0]
		else:
			info = CommonInfo.objects.get(user_id = currentUserId)

		SEX_TYPE = {
			"": "---------",
			"B": "Boy",
			"G": "Girl"
		}
		BLOOD_TYPE = {
			'': "---------",
			'A': 'A',
			'B': 'B',
			'O': 'O',
			'AB': 'AB'
			}
		return render_to_response('main-editinfo.html',
			{'userList': userList, 'currentUser': currentUser,
			 'info': info, 'SEX_TYPE': SEX_TYPE, 'BLOOD_TYPE': BLOOD_TYPE},
			context_instance=RequestContext(request))

	infoqs = CommonInfo.objects.filter(user_id = userId)
	if infoqs:
		info = infoqs[0]
	else:
		return main_view(request)

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

	return info_view(request, userId)

def password_view(request):
	if request.session.get('user_id', -1) == -1:
		return render_to_response('signin.html', context_instance=RequestContext(request))

	if 'oldpassword' not in request.POST:
		currentUserId = request.session.get('user_id')
		currentUser = User.objects.get(id = currentUserId)
		return render_to_response('password.html', {'currentUser':currentUser}, context_instance=RequestContext(request))
	
	oldpw = request.POST.get('oldpassword')
	newpw = request.POST.get('newpassword')
	#confirmpw = request.POST.get('confirmpassword')
	# js confirm newpw is equal to confirmpw
	
	currentUserId = request.session.get('user_id')
	currentUser = User.objects.get(id = currentUserId)
	if oldpw == currentUser.password:
		currentUser.password = newpw
		currentUser.save()

	return main_view(request)

def newuser_view(request):
	if request.session.get('user_id', -1) == -1:
		return render_to_response('signin.html', context_instance=RequestContext(request))

	if 'account' in request.POST:
		#if User.objects.filter(account = account):

		account = request.POST.get('account')
		password = request.POST.get('password')
		cname = request.POST.get('cname')

		user = User(account=account, password = password, cname = cname, role = 'C')
		user.save()
		info = CommonInfo(user=user)
		info.ename=""
		info.birthday =time.strftime('%Y-%m-%d',time.localtime(time.time()))
		info.sex = ""
		info.bloodtype = ""
		info.cellphone = ""
		info.email = ""
		info.mailbox = ""
		info.homeaddr = ""
		info.currentaddr = "Mars"
		info.save()
		return main_view(request)

	currentUserId = request.session.get('user_id')
	currentUser = User.objects.get(id = currentUserId)

	return render_to_response('newuser.html',{'currentUser': currentUser }, context_instance = RequestContext(request))

def deleteuser_view(request):
	if 'userId' in request.GET:
		userId = request.GET.get('userId')

	userqs = User.objects.filter(id = userId)
	if userqs:
		user = userqs[0]
		user.delete()

	userList = User.objects.all()

	res = HttpResponse()
	res['Content-Type'] = "text/javascript"
	res.write(serializers.serialize("json", userList))

	return res