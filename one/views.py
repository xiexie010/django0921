from django.shortcuts import render,redirect

from .forms import Form1
from .models import UserInfo
from django.http import HttpResponse
from .tables import UserInfoTable,TableView
from django_tables2 import RequestConfig
import datetime
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.core import serializers

def home(request):
    users0=UserInfo.objects.all();
    # return render(request, 'one/home.html',{'users':users})
    current_page = request.GET.get('page')
    paginator = Paginator(users0, 10)
    # per_page: 每页显示条目数量
    # count:    数据总个数
    # num_pages:总页数
    # page_range:总页数的索引范围，如: (1,10),(1,200)
    # page:     page对象(是否具有上一页，下一页)
    try:
        users = paginator.page(current_page)
        # has_next              是否有下一页
        # next_page_number      下一页页码
        # has_previous          是否有上一页
        # previous_page_number  上一页页码
        # object_list           分页之后的数据列表
        # number                当前页
        # paginator             paginator对象
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        users = paginator.page(1)
    return render(request, 'one/home.html', {'users': users})

def cookie_auth(func):
    def weaper(request,*args,**kwargs):
        # cookies = request.get_signed_cookie('k', salt='zhanggen')
        # cookies=request.COOKIES.get("tile")
        # if cookies == 'zhanggen':
        #     return func(request)
        if request.session.get('is_login'):
            return func(request)
        else:
            return render(request, 'one/login.html')
    return weaper

@cookie_auth
def index(request):
    # for i in range(21):
    #     user=UserInfo(username="testtest"+str(i),password=222)
    #     user.save()
    table=UserInfoTable(UserInfo.objects.all())
    RequestConfig(request,paginate={'per_page':8}).configure(table)


    return render(request, 'one/index.html',{'users':table})



def login(request):
    return render(request, 'one/login.html')


def register(request):
    return render(request, 'one/register.html')

def uploadform(request):
    if request.method == "POST":  # 这里POST一定要大写
        # 通常获取请求信息
        # request.POST.get("user",None)
        # request.POST.get("pwd",None)
        # 获取请求内容，做验证
        f = Form1(request.POST)  # request.POST：将接收到的数据通过Form1验证
        if f.is_valid():  # 验证请求的内容和Form1里面的是否验证通过。通过是True，否则False。
            print(f.cleaned_data)  # cleaned_data类型是字典，里面是提交成功后的信息
            if(f.instance.username=="11" and f.instance.password=="12"):
                # obj = redirect("/one/login")
                # # obj.set_cookie("tile","zhanggen",max_age=1,)
                # now = datetime.datetime.utcnow()
                # delta = timedelta(seconds=5)
                # value = now + delta
                # obj.set_cookie("tile", "zhanggen", expires=value, path='/', domain=None, secure=False, httponly=False)
                # obj.set_signed_cookie('k', 'v', salt="zhanggen", )

                request.session.set_expiry(30*60)  # session认证时间为10s，10s之后session认证失效
                request.session['username'] = f.instance.username  # user的值发送给session里的username
                request.session['is_login'] = True  # 认证为真
                return HttpResponse("ok")
            else:
                return HttpResponse("no")

        else:  # 错误信息包含是否为空，或者符合正则表达式的规则
            print(type(f.errors), f.errors)  # errors类型是ErrorDict，里面是ul，li标签
            # return render(request, "account/form1.html", {"error": f.errors})
        f.save()
    return render(request, "one/index.html")

def createUser(request):
    if request.method == "POST":
        print("createUser:"+request.POST.get("username"))
        print("test git")
        f = Form1(request.POST)
        if f.is_valid():
            print("createUser--ok")
            user = UserInfo(username=f.instance.username , password=f.instance.password)
            user.save()
            return HttpResponse("ok")
        else:
            print("createUser--no")
            return HttpResponse("no")
    else:
        return HttpResponse("no")

def getUserFromId(request,userid):
    print("getUserFromId"+str(userid))
    user=UserInfo.objects.get(id=userid)
    result = serializers.serialize("json", [user])
    return HttpResponse(result)