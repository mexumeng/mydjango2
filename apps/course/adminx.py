__author__ = 'xumeng'
__date__ = '2018/7/3 19:31'
import xadmin
from .models import Course, CourseResource, Lesson, Video


class CourseAdmin:

    list_display = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums', 'add_time']
    # 显示排序
    ordering = ['-click_nums']
    # 设置只读
    readonly_fields = ['click_nums']
    # 设置不显示到管理界面
    exclude = ['fav_nums']


class LessonAdmin:

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoAdmin:

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin:

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
