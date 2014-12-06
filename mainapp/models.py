# coding=utf-8
from django.conf import settings
from django.db import models
from django.contrib import admin

# 以下为自定义 Auth User 模型，因为自定义模型需要重新实现权限管理，所以目前直接使用Django定义的User模型
# settings.AUTH_USER_MODEL缺省为Django定义的User
#
# from django.contrib.auth.models import User,\
#     BaseUserManager, AbstractBaseUser, PermissionsMixin
# from django.utils import timezone
#
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('account', 'role')
# class AuthUserManager(BaseUserManager):
#     def create_user(self, email, password):
#         if not email:
#             raise ValueError("Account Email error")
#
#         user = self.model(
#             email = AuthUserManager.normalize_email(email),
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#
#         return user
#
#     def create_superuser(self, email, password):
#         user = self.create_user(
#             email = email,
#             password = password,
#         )
#
#         user.is_active = True
#         user.is_staff = True
#         user.is_admin = True
#
#         user.save(using = self._db)
#
#         return user
#
#
# class AuthUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=40, unique=True, db_index=True,)
#     USERNAME_FIELD = 'email'
#     is_active = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#
#     objects = AuthUserManager()
#
#     def get_full_name(self):
#         return self.email
#
#     def get_short_name(self):
#         return self.email
#
#     def __unicode__(self):
#         return self.email


class CommonInfo(models.Model):
    SEX_TYPE = (
        ('', '------'),
        ('B', 'Boy'),
        ('G', 'Girl'),
    )
    # choice 只能使用tuple
    BLOOD_TYPE = (
        ('', '------'),
        ('A', 'A'),
        ('B', 'B'),
        ('O', 'O'),
        ('AB', 'AB'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    cname = models.CharField(max_length=20)
    ename = models.CharField(max_length=30, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_TYPE, null=True, blank=True)
    bloodtype = models.CharField(max_length=2, choices=BLOOD_TYPE, null=True, blank=True)
    cellphone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    mailbox = models.CharField(max_length=100, null=True, blank=True)
    homeaddr = models.CharField(max_length=100, null=True, blank=True)
    currentaddr = models.CharField(max_length=100, null=True, blank=True)


    def __unicode__(self):
        return self.cname


# 定义Admin界面，Info信息显示列
class InfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'cname', 'email',)

#admin.site.register(User, UserAdmin)
admin.site.register(CommonInfo, InfoAdmin)
