
# 同学录
基于Django的一个Web App，用于同学信息的维护，以及班级活动的管理（正在实现）。

## 运行需求
1. Python 2.7.x
2. Django 1.5+
3. Python-MySQLdb 1.2.3+
4. MySQL


## 运行
1. 修改`settings.py`中关于MySQL用户名和密码的设置
2. 在MySQL中创建一个名为`app_classmates`的空数据库
3. 在应用根目录下运行`manage.py syncdb`初始化数据库，会要求设置网站管理员账号和密码
4. 运行`manage.py runserver`
