from django.urls import path, re_path
from apps.course.views import CourseHomeView, VideoPlay, CourseLessonView, CourseComentView, AddCommentView, CourseDetailView
__author__ = "xumeng"
__date__ = "2018/8/4 15:58"
app_name = 'course'
urlpatterns = [
    path('list/', CourseHomeView.as_view(), name='cou_list'),
    re_path('detail/(?P<cou_id>\d+)/', CourseDetailView.as_view(), name='cou_detail'),
    re_path('lesson/(?P<cou_id>\d+)/', CourseLessonView.as_view(), name='cou_lesson'),
    re_path('comment/(?P<cou_id>\d+)/', CourseComentView.as_view(), name='cou_comment'),
    path('add_comment/', AddCommentView.as_view(), name='add_comment'),
    re_path('play/(?P<video_id>\d+)/', VideoPlay.as_view(), name='cou_play'),
]
