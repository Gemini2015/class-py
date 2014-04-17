from django.db import models
from django.contrib import admin
# Create your models here.

class User(models.Model):
	ROLE_TYPE = (
		('A', 'Admin'),
		('C', 'CommonUser'),
		)
	account = models.CharField(max_length = 30, unique=True)
	password = models.CharField(max_length = 200)
	cname = models.CharField(max_length = 20)
	role = models.CharField(max_length = 1, choices = ROLE_TYPE)

	def __unicode__(self):
		return self.account

class UserAdmin(admin.ModelAdmin):
	list_display = ('account', 'role')

class CommonInfo(models.Model):
	SEX_TYPE = (
		('B', 'Boy'),
		('G', 'Girl'),
		)
	BLOOD_TYPE = (
		('A', 'A'),
		('B', 'B'),
		('O', 'O'),
		('AB', 'AB'),
		)

	user = models.ForeignKey(User)
	#cname = models.CharField(max_length = 20)
	ename = models.CharField(max_length = 30, null = True, blank = True)
	birthday = models.DateField(null = True, blank = True)
	sex = models.CharField(max_length = 1, choices = SEX_TYPE, null = True, blank = True)
	bloodtype = models.CharField(max_length = 2, choices = BLOOD_TYPE, null = True, blank = True)
	cellphone = models.CharField(max_length = 20, null = True, blank = True)
	email = models.EmailField(null = True, blank = True)
	mailbox = models.CharField(max_length = 100, null = True, blank = True)
	homeaddr = models.CharField(max_length = 100, null = True, blank = True)
	currentaddr = models.CharField(max_length = 100, null = True, blank = True)

	def __unicode__(self):
		return self.user.cname


admin.site.register(User, UserAdmin)
admin.site.register(CommonInfo)
