from django.shortcuts import render, HttpResponse, redirect
from app01.forms import *
from django.contrib.auth.hashers import make_password
from app01 import models
from django.contrib.auth import authenticate, login, logout
from django.db.models import F
import time
from django.db.models import Count
# Create your views here.
from django.db import transaction

import json


def log_in(request):
    '''登陆'''
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        data = request.POST
        form = LoginForm(data=data)
        validcode = request.POST.get('validcode')

        if not form.is_valid():
            return HttpResponse(json.dumps(dict(form.errors)))
        if validcode.upper() != request.session["keepValidCode"].upper():
            return HttpResponse(json.dumps('codeError'))

        user = authenticate(**form.cleaned_data)
       
        if not user:

            return HttpResponse(json.dumps({'flag': False, 'msg': "用户名或者密码错误"}))

        else:
            login(request, user)  
        return HttpResponse(json.dumps({'flag': True}))


def log_out(request):
    '''注销'''
    logout(request)
    return redirect('/login/')


def home(request, *args, **kwargs):
    '''博客园首页'''
    if kwargs:
        '''博客园站点分类显示'''
        print(kwargs.get("siteCategory"))
        articles = models.Article.objects.filter(siteCategory__title=kwargs.get("siteCategory"))
    else:
        articles = models.Article.objects.all()

   
    siteMenu1 = models.SiteMenu.objects.all().annotate(count=Count('sitecategory__article')).values_list('title',
                                                                                                         'count')

    siteMenu2 = models.SiteMenu.objects.all()

    siteMenu = {}
    for obj in siteMenu2:
        for i in siteMenu1:
            if obj.title == i[0]:
                siteMenu[obj] = i[1]
 
  

    return render(request, 'home.html', {'articles': articles, 'siteMenu': siteMenu})


def reg(request):
    if request.is_ajax():
        form = RegForm(data=request.POST)
        regResponse = {"user": None, "errorsList": None}
        if not form.is_valid():
            regResponse["errorsList"] = form.errors

        else:
            username = request.POST.get('username')
            password = make_password(request.POST.get('password'))
            nickname = request.POST.get('nickname')
            tel = request.POST.get('tel')
            email = request.POST.get('email')
            avatar_img = request.FILES.get('avatar')
            if not avatar_img:
                user_obj = models.UserInfo.objects.create(username=username, password=password, email=email,
                                                               nickname=nickname, tel=tel)
                regResponse["user"] = user_obj.username
            else:
                user_obj = models.UserInfo.objects.create_user(username=username, password=password, email=email,
                                                               avatar=avatar_img, nickname=nickname, tel=tel)
                regResponse["user"] = user_obj.username
        return HttpResponse(json.dumps(regResponse))
    form = RegForm()
    return render(request, 'reg.html', {'form': form})


def validcode(request):
    import random
    from PIL import Image, ImageDraw, ImageFont
    from io import BytesIO

    img = Image.new(mode='RGB', size=(120, 40),
                    color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw = ImageDraw.Draw(img, 'RGB')
    font = ImageFont.truetype('app01/static/font/kumo.ttf', 25)
    valid_list = []
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_upper_alp = chr(random.randint(65, 90))
        random_lower_alp = chr(random.randint(97, 122))
        valid_ele = random.choice([random_num, random_upper_alp, random_lower_alp])
        valid_list.append(valid_ele)
        draw.text([5 + i * 24, 10], valid_ele, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                  font=font)

      
    for i in range(40):
        draw.point([random.randint(0, 120), random.randint(0, 40)],
                   fill=(random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)))

  
    for i in range(40):
        draw.point([random.randint(0, 120), random.randint(0, 40)],
                   fill=(random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)))
        x = random.randint(0, 120)
        y = random.randint(0, 40)
        draw.arc((x, y, x + 4, y + 4), 0, 90,
                 fill=(random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)))


    for i in range(5):
        x1 = random.randint(0, 120)
        y1 = random.randint(0, 40)
        x2 = random.randint(0, 120)
        y2 = random.randint(0, 40)

        draw.line((x1, y1, x2, y2), fill=(random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)))

    f = BytesIO()
    img.save(f, 'png')
    data = f.getvalue()
    valid_str = ''.join(valid_list)     
    print(valid_str)
    request.session["keepValidCode"] = valid_str   


    return HttpResponse(data)


def homeSite(request, username, **kwargs):
    '''个人博客首页'''
   
    current_user = models.UserInfo.objects.filter(username=username).first()
    status=True


    if not current_user:
        return render(request, 'notFound.html')

   
    current_blog = current_user.blog
    tag = models.Tag.objects.filter(blog=current_blog).annotate(c=Count('article__nid')).values_list('title', 'c')
    
    data = models.Article.objects.filter(user=current_user).extra(
        select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(
        Count("nid"))  


    if not kwargs:
     
        article_list = models.Article.objects.filter(user=current_user)
    if kwargs.get("condition") == "category":
        article_list = models.Article.objects.filter(user=current_user, category__title=kwargs.get("para"))
    elif kwargs.get("condition") == "tag":
        article_list = models.Article.objects.filter(user=current_user, tags__title=kwargs.get("para"))
    elif kwargs.get("condition") == "date":
        year, month = kwargs.get("para").split('/')
        article_list = models.Article.objects.filter(user=current_user, create_time__year=year, create_time__month=month)


    return render(request, "homeSite.html", locals())

def articleDetail(request ,username, **kwargs):
    '''文章具体内容页面'''
    current_user = models.UserInfo.objects.filter(username=username).first()
    if not current_user:
        return render(request, 'notFound.html')
    current_blog = current_user.blog

    
    article_list = models.Article.objects.filter(user=current_user)

  
    tag = models.Tag.objects.filter(blog=current_blog).annotate(c=Count('article__nid')).values_list('title', 'c')

    
    data = models.Article.objects.filter(user=current_user).extra(
        select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(
        Count("nid"))


   
    content_list = models.Article.objects.filter(nid=kwargs.get('para')).values_list('nid', 'title',
                                                                                     'articledetail__content',
                                                                                     'create_time', 'read_count',
                                                                                     'comment_count', 'up_count',
                                                                                     'down_count')
  
    comment_list=models.Article.objects.filter(nid=kwargs.get('para')).first().article_comment.all()






    return render(request, "article_content.html", locals())





def poll(request):
    
    pollResponse = {"state": True, "is_repeat": None}
    if not request.user.is_authenticated():
        pollResponse["state"] = False
    else:
        user_id = request.user.nid
        article_id = request.POST.get('article_id')
        try:
            with transaction.atomic(): 
                models.ArticleUp.objects.create(user_id=user_id, article_id=article_id)
                models.Article.objects.filter(nid=article_id).update(up_count=F('up_count') + 1)
        except Exception as e:
            print(e)
            pollResponse["is_repeat"] = True
    return HttpResponse(json.dumps(pollResponse))


def comment(request):

    content = request.POST.get('comment').strip()
    article_id = request.POST.get('article_id')
    commentResponse = {"state": True,'comment_list':None,'parent_comment_id':None}
    if not request.user.is_authenticated() or len(content)==0:
        commentResponse["state"] = False
        return commentResponse
    else:
        user_id = request.user.nid
        pid = request.POST.get('parent_comment_id')
       
        if pid: 
            with transaction.atomic():
                comment_obj = models.Comment.objects.create(user_id=user_id, article_id=article_id, content=content,parent_comment_id=pid)
                models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count') + 1)
                commentResponse["parent_comment_content"] = comment_obj.parent_comment.content
                commentResponse["parent_comment_username"] = comment_obj.parent_comment.user.username
              
                commentResponse['parent_comment_id']=pid
               

        else:  
            with transaction.atomic():
                comment_obj=models.Comment.objects.create(user_id=user_id,article_id=article_id,content=content)
                models.Article.objects.filter(nid=article_id).update(comment_count=F('comment_count')+1)
       
        commentResponse['comment_time']=comment_obj.create_time.strftime('%Y-%m-%d %H:%M') 
        commentResponse['comment_id'] = comment_obj.nid
        

    return HttpResponse(json.dumps(commentResponse))


def commentTree(request,article_id):
    
    all = models.Comment.objects.filter(article_id=article_id).values('nid', 'content', 'parent_comment_id','user__avatar','user__username','create_time')
   
    d = {}
    for i in all:
        d[i['nid']] = i

    commentTree = []
    for k, v in d.items():
        v["chidren_commentList"] = []
        pid = v['parent_comment_id']
        if not pid:
            commentTree.append(v)
        else:
          
            d[pid]['chidren_commentList'].append(v)
           
    from django.http import JsonResponse
    return JsonResponse(commentTree,safe=False) 


def manage(request):
    if not request.user.is_authenticated():
        return redirect("/login/")
    article_list = models.Article.objects.filter(user=request.user).all()

    current_user=request.user
    current_blog = current_user.blog

   
    from django.db.models import Count, Sum

    category_list = models.Category.objects.filter(blog=current_blog).annotate(c=Count("article__nid")).values_list("title", "c")

    return render(request, "manage_base.html", {"article_list": article_list,'category_list':category_list,'current_user':current_user})

import datetime

def addArticle(request):

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            title = article_form.cleaned_data.get("title")
            content = article_form.cleaned_data.get("content")
            article_obj = models.Article.objects.create(title=title, desc=content[0:30],
                                                        create_time=datetime.datetime.now(), user=request.user)
            models.ArticleDetail.objects.create(content=content, article=article_obj)
        else:
            pass

        return HttpResponse("添加成功")

    article_form = ArticleForm()
    return render(request, "addArticle.html", {"article_form": article_form})


def uploadFile(requset):
   
    file_obj=requset.FILES.get('imgFile')
    file_name=file_obj.name

    from django.conf import settings
    import os
    path=os.path.join(settings.MEDIA_ROOT,'article_uploads',file_name)
    with open(path,'wb') as f:
        for i in file_obj.chunks():
            f.write(i)

    response={
        'error':0,
        'url':'/media/article_uploads/'+file_name+'/'
    }
   

    import json
    return HttpResponse(json.dumps(response))