__author__ = 'xumeng'
__date__ = '2018/7/3 17:05'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord
from .models import Banner


class BaseSetting:
    enable_themes = True
    use_bootswatch = True


class GlobalSettings:
    site_title = '孟哥后台管理系统'
    site_footer = '孟哥网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin:
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['email', 'code']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    # 设置图标
    model_icon = 'fa fa-codiepie'


class BannerAdmin:
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
