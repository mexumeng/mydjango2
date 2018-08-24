from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q
from apps.oragnization.models import CityDict, CourseOrg, Teacher
from apps.course.models import Course
from pure_pagination import Paginator, PageNotAnInteger
from apps.oragnization.forms import UserAskForm
from apps.operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    def get(self, request):
        citys_all = CityDict.objects.all()
        orgs_all = CourseOrg.objects.all()
        city_id = request.GET.get('city', '')
        hot_orgs = orgs_all.order_by('-click_nums')[:3]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            orgs_all = CourseOrg.objects.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords))
        if city_id:
            orgs_all = orgs_all.filter(city_id=int(city_id))
        category = request.GET.get('ct', '')
        if category:
            orgs_all = orgs_all.filter(category=category)
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                orgs_all = orgs_all.order_by('-students')
            elif sort == 'courses':
                orgs_all = orgs_all.order_by('-course_nums')
        orgs_nums = orgs_all.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs_all, 5, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html',
                      {'citys_all': citys_all,
                       'orgs_all': orgs,
                       'orgs_nums': orgs_nums,
                       'city_id': city_id,
                       'category': category,
                       'hot_orgs': hot_orgs,
                       'sort': sort,


                       }
                      )


class UserAskView(View):
    def post(self, request):
        userask_forms = UserAskForm(request.POST)
        if userask_forms.is_valid():
            use_ask = userask_forms.save(commit=True)
            return HttpResponse('{"status": "success" }', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"信息输入有误"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:2]
        all_teachers = course_org.teacher_set.all()[:2]
        wherepage = 'home'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'wherepage': wherepage,
            'has_fav': has_fav,

        })


class OrgCourseView(View):
    def get(self, request, org_id):
        wherepage = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'wherepage': wherepage,
            'has_fav': has_fav
        })


class OrgDescView(View):
    def get(self, request, org_id):
        wherepage = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'wherepage': wherepage,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        wherepage = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'wherepage': wherepage,
            'has_fav': has_fav

        })


class AddFavCoursesView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        fav_id = int(fav_id)
        fav_type = int(fav_type)
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录！"}', content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            exist_records.delete()
            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                    course.save()
            elif fav_type == 2:
                org = CourseOrg.objects.get(id=fav_id)
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                    org.save()
            elif fav_type == 3:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                    teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type > 0:
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                elif fav_type == 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_nums += 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()


                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        teachers_all = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        rank_teachers = teachers_all.order_by('-fav_nums')[:5]
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            teachers_all = Teacher.objects.filter(name__icontains=search_keywords)
        if sort:
            if sort == 'hot':
                teachers_all = teachers_all.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(teachers_all, 3, request=request)
        teachers = p.page(page)
        return render(request, 'teachers-list.html', {
            'teachers': teachers,
            'rank_teachers': rank_teachers,
            'sort': sort,
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        has_teacher_fav = False
        has_org_fav = False
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        org = CourseOrg.objects.get(teacher=teacher)
        courses = Course.objects.filter(teacher=teacher)
        rank_teachers = Teacher.objects.filter(org=org).order_by('-fav_nums')[:3]
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                has_org_fav = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'courses': courses,
            'rank_teachers': rank_teachers,
            'has_teacher_fav': has_teacher_fav,
            'has_org_fav': has_org_fav,


        })
