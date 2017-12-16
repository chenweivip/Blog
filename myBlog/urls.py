"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
from django.views.static import serve
from django.conf import settings
from app.views import pcgetcaptcha
from app.views import pcvalidate
from app.views import pcajax_validate
from django.conf.urls import url, include
from app.views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^reg/', views.reg),
    url(r'^login/', views.log_in),
    url(r'^logout/', views.log_out),
    # url(r'^index/', views.index),

    # url(r'^base/', views.home),

    url(r'^validcode/', views.validcode),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    url(r'^pc-geetest/register', pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/validate$', pcvalidate, name='pcvalidate'),
    url(r'^pc-geetest/ajax_validate', pcajax_validate, name='pcajax_validate'),

    # 博客园站点分类
    url(r'^cate/(?P<siteCategory>.*)/$', views.home),  # # index(requset,site_article_category=python)

    # 个人站点首页
    url(r'^blog/', include('app01.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^uploadFile/$', views.uploadFile),

]
