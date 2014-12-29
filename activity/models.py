# coding=utf-8
from django.db import models
from django.conf import settings
from django.contrib import admin
from mainapp.models import CommonInfo


# Create your models here.
# Activity 模型
class Activity(models.Model):
    # 活动标题
    title = models.CharField(max_length=100, blank=False)
    # 创建者，不创建反向关系
    creator = models.ForeignKey(CommonInfo, blank=False, related_name='+')
    # 组织者
    organizer = models.ForeignKey(CommonInfo, blank=True, related_name='+')
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
    list_display = ('id', 'title', 'creator', 'organizer', 'datetime', 'location', 'content', 'status')

admin.site.register(Activity, ActivityAdmin)


class UserActivity(models.Model):
    """
    用来记录用户参与活动的记录
    """
    # 用户
    user = models.ForeignKey(CommonInfo, blank=False)
    # 板块
    SECTION_TYPE = (
        (1, 'Activity'),
        (2, 'Other'),
    )
    section = models.SmallIntegerField(choices=SECTION_TYPE, blank=False)
    # 项的ID
    item = models.IntegerField(blank=False)
    # 是否参与
    is_participate = models.BooleanField()


class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'section', 'item', 'is_participate')

admin.site.register(UserActivity, UserActivityAdmin)


class Comment(models.Model):
    """
    定义整个系统的评论
    """
    # 定义评论所属板块
    section = models.SmallIntegerField(choices=UserActivity.SECTION_TYPE, blank=False)
    # 对应评论项的ID
    item = models.IntegerField(blank=False)
    # 评论人员
    commentator = models.ForeignKey(CommonInfo, blank=False)
    # 是否匿名评论
    is_anonymous = models.BooleanField()
    # 时间
    datetime = models.DateTimeField()
    # 内容
    content = models.CharField(max_length=200, blank=False)
    # 其他信息
    remark = models.CharField(max_length=100, blank=True)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('section', 'item', 'commentator', 'is_anonymous', 'datetime', 'content', 'remark')

admin.site.register(Comment, CommentAdmin)