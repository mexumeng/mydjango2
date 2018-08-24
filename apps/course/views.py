from django.shortcuts import render
from django.views.generic import View
from django.db.models import Q
from apps.course.models import Course, Lesson, Video
from apps.operation.models import UserFavorite, CourseComents, UserCourse
from pure_pagination import Paginator, PageNotAnInteger
from django.http import HttpResponse
from utils.mixin_util import LoginRequiredMixin

# Create your views here.


class CourseHomeView(View):
    def get(self, request):
        sort = request.GET.get('sort', '')
        courses = Course.objects.all().order_by('-add_time')
        hot_courses = courses.order_by('-click_nums')[:3]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            courses = Course.objects.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))
        if sort:
            if sort == 'hot':
                courses = courses.order_by('-click_nums')
            elif sort == 'students':
                courses = courses.order_by('-students')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, 3, request=request)
        cous = p.page(page)
        return render(request, 'course-list.html', {
            'cous': cous,
            'hot_courses': hot_courses,
            'sort': sort,
        })


class CourseDetailView(View):
    def get(self, request, cou_id):
        course = Course.objects.get(id=int(cou_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        relate_courses = []
        if tag:
            relate_courses = Course.objects.filter(tag=tag)
            relate_courses = relate_courses.filter(~Q(id=course.id))
        if relate_courses:
            relate_courses = relate_courses[:1]
        else:
            relate_courses = []
        has_cou_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_org_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_cou_fav = True
        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_org_fav': has_org_fav,
            'has_cou_fav': has_cou_fav,
        })


class CourseLessonView(LoginRequiredMixin, View):
    def get(self, request, cou_id):
        course = Course.objects.get(id=int(cou_id))
        if not UserCourse.objects.filter(user=request.user, course=course):
            course.students += 1
            course.save()
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_courses = UserCourse.objects.filter(course=course)
        users_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=users_ids)
        courses_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=courses_ids)[:5]
        lessons = Lesson.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'lessons': lessons,
            'relate_courses': relate_courses,
        })


class CourseComentView(LoginRequiredMixin, View):
    def get(self, request, cou_id):
        course = Course.objects.get(id=int(cou_id))
        user_courses = UserCourse.objects.filter(course=course)
        users_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=users_ids)
        courses_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=courses_ids)[:5]
        lessons = Lesson.objects.filter(course=course)
        comments = CourseComents.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'lessons': lessons,
            'all_comments': comments,
            'relate_courses': relate_courses,
        })


class AddCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comments', '')
        if int(course_id) > 0 and comment:
            course_comment = CourseComents()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comments = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')


class VideoPlay(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = Course.objects.get(lesson=video.lesson)
        user_courses = UserCourse.objects.filter(course=course)
        users_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=users_ids)
        courses_ids = [user_course.course.id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=courses_ids)[:5]
        lessons = Lesson.objects.filter(course=course)
        return render(request, 'course-play.html', {
            'course': course,
            'relate_courses': relate_courses,
            'video': video,
            'lessons': lessons,
        })
