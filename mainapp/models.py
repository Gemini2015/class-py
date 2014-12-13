# coding=utf-8
from django.conf import settings
from django.db import models
from django.contrib import admin

# 以下为自定义 Auth User 模型，因为自定义模型需要重新实现权限管理，所以目前直接使用Django定义的User模型
# settings.AUTH_USER_MODEL缺省为Django定义的User
#
# from django.contrib.auth.models import User,\
# BaseUserManager, AbstractBaseUser, PermissionsMixin
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


# 用户信息模型
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
    ename = models.CharField(max_length=30, blank=True)
    birthday = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_TYPE, blank=True)
    bloodtype = models.CharField(max_length=2, choices=BLOOD_TYPE, blank=True)
    cellphone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    mailbox = models.CharField(max_length=100, blank=True)
    homeaddr = models.CharField(max_length=100, blank=True)
    currentaddr = models.CharField(max_length=100, blank=True)


    def __unicode__(self):
        return self.cname


# 定义Admin界面，Info信息显示列
class InfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'cname', 'email',)

#admin.site.register(User, UserAdmin)
admin.site.register(CommonInfo, InfoAdmin)


# Activity 模型
class Activity(models.Model):
    # 活动标题
    title = models.CharField(max_length=100, blank=False)
    # 创建者，不创建反向关系
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, related_name='+')
    # 组织者
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, related_name='+')
    # 时间
    datetime = models.DateTimeField()
    # 地点
    location = models.CharField(max_length=100, blank=True)
    # 内容
    content = models.TextField(blank=True)
    # 状态: 讨论中，已发布，已结束，删除(服务器后台做记录，除非超级管理员删除)
    ACTIVITY_STATUS = (
        (1, 'Discussing'),
        (2, 'Published'),
        (3, 'Finished'),
        (4, 'Deleted'),
    )
    status = models.SmallIntegerField(choices=ACTIVITY_STATUS, blank=False)

    def __unicode__(self):
        return self.title + self.datetime.__str__() + self.location + self.status.__str__()

    def __str__(self):
        return self.__unicode__()

    # def __init__(self, *args, **kwargs):
    #     self.creator = kwargs.get('creator', None)
    #     self.title = kwargs.get('title', '')
    #     self.organizer = kwargs.get('organizer', None)
    #     self.datetime = kwargs.get('datetime', None)
    #     self.location = kwargs.get('location', '')
    #     self.content = kwargs.get('content', '')
    #     self.status = kwargs.get('status', 1)
    #     models.Model.__init__(self, *args, **kwargs)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'organizer', 'datetime', 'location', 'content', 'status')

admin.site.register(Activity, ActivityAdmin)


class Comments(models.Model):
    """
    定义整个系统的评论
    """
    # 定义评论所属板块
    SECTION_TYPE = (
        (1, 'Activity'),
        (2, 'Other'),
    )
    section = models.SmallIntegerField(choices=SECTION_TYPE, blank=False)
    # 对应评论项的ID
    item = models.IntegerField(blank=False)
    # 评论人员
    commentator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False)
    # 是否匿名评论
    is_anonymous = models.BooleanField()
    # 时间
    datetime = models.DateTimeField()
    # 内容
    comment = models.CharField(max_length=200, blank=False)
    # 其他信息
    remark = models.CharField(max_length=100, blank=True)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('section', 'item', 'commentator', 'is_anonymous', 'datetime', 'comment', 'remark')

admin.site.register(Comments, CommentsAdmin)