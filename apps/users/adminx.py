#-*- coding:utf-8 -*-

import xadmin
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


#设置主题
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    model_icon = 'fa fa-envelope-open'
    # fa - envelope - open


#设置页头页尾
class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = 'accordion'  #可折叠目录


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'add_time']
    search_fields = ['title', 'image', 'url' ]
    list_filter = ['title', 'image', 'url', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner , BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
