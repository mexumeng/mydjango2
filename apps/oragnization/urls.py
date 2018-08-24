from django.urls import path, re_path
from apps.oragnization.views import OrgView, UserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, \
    AddFavCoursesView, TeacherListView, TeacherDetailView


app_name = 'oragnization'
urlpatterns = [
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/', UserAskView.as_view(), name='add_ask'),
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name='org_home'),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name='course_org'),
    re_path('desc/(?P<org_id>\d+)/', OrgDescView.as_view(), name='desc_org'),
    re_path('org_teacher/(?P<org_id>\d+)/', OrgTeacherView.as_view(), name='teacher_org'),
    path('add_fav/', AddFavCoursesView.as_view(), name='add_fav'),
    path('teacher/list/', TeacherListView.as_view(), name='teacher_list'),
    re_path('teacher/detail/(?P<teacher_id>\d+)/', TeacherDetailView.as_view(), name='teacher_detail'),







]
