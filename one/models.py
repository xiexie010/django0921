from django.db import models

# Create your models here.

class UserInfo(models.Model):
 #创建表的字段
    username = models.CharField(max_length=16,verbose_name="账号") #创建一个字段，类型为字符串类型，最大长度为16
    password = models.CharField(max_length=32,verbose_name="密码") #创建一个字段，类型为字符串类型，最大长度为32