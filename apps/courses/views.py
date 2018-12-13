#-*- coding:utf-8 -*-

from django.core.paginator import PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator

# Create your views here.

from courses.models import Course, CourseResource, Video
from operation.models import UserFavourite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")

        #热门课程推荐
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        #对课程排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == "students":
                all_courses.order_by("-students")
            elif sort == "hot":
                all_courses.order_by("-hot")

        #对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 9, request=request)
        sort
        courses = p.page(page)
        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums += 1
        course.save()

        #检查收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavourite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            elif UserFavourite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]

        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_org": has_fav_org,
            "has_fav_course": has_fav_course
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        #点击了‘开始学习’，学习人数就加1
        course.students += 1
        course.save()

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        #取出用户所有课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程的id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        #获取该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            'all_resources':all_resources,
            'relate_courses': relate_courses
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        #判断用户登录状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "") #这是ajax提交的信息，如果不为空
        if course_id>0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course     #把评论和课程关联起来
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status": "success", "msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg":"添加失败"}', content_type="application/json")


class CommentsView(LoginRequiredMixin, View):
    """
    评论页面
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
        })


class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self, request, video_id):
        video  = Video.objects.get(id=int(video_id)) #todo 确认是Course还是Video
        course = video.lesson.course
        course.students += 1
        course.save()
        #查询该用户是否关联课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        user_coursers = UserCourse.objects.filter(course=course)
        user_ids = [user_courser.user.id for user_courser in user_coursers]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有的额课程id
        course_ids = [user_courser.course.id for user_courser in all_user_courses]
        #获取该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "relate_courses": relate_courses,
            "video": video,
            "all_resources": all_resources
        })



























