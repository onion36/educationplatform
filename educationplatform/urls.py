#-*- coding:utf-8 -*-
"""educationplatform URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
from django.views.static import serve

from organization.views import OrgView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView,ModifyPwdView, LogoutView
from educationplatform.settings import MEDIA_ROOT
from users.views import IndexView



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),

    #配置上传文件的访问处理函数（media文件）
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    #配置上传文件的访问处理函数（media文件）
    # url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    #验证码
    url(r'^captcha/', include('captcha.urls')),
    #邮箱注册
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    #找回密码
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    #重置密码验证码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    #找回密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),


    #课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),
    #课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),
    #课程相关url配置
    url(r'^teacher/', include('courses.urls', namespace="course")),
    # 用户相关url配置
    url(r'^users/', include('users.urls', namespace="users")),
    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]
#  全局404处理函数
handler404 = 'users.views.page_not_found'
#  全局500处理函数
handler500 = 'users.views.page_error'

