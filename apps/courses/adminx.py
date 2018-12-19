#-*- coding:utf-8 -*-
import xadmin

from courses.models import Course, Lesson, Video, CourseResource, BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image','click_nums', 'add_time', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image','click_nums', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums']
    exclude = ['click_nums']
    inlines = [LessonInline, CourseResourceInline]
    list_editable = ['degree', 'desc']
    style_fields = {"detail": "ueditor"}
    import_excel = True
    # refresh_times = [3, 5]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        #在保存课程的时候，统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image','click_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_times', 'students', 'fav_nums', 'image','click_nums', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['fav_nums']
    exclude = ['click_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs



class LessonAdmin(object):
    list_display = ['course', 'name','add_time' ]
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name','add_time' ]


class VideoAdmin(object):
    list_display = ['lesson', 'name','add_time' ]
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name','add_time' ]


class CourseResourceAdmin(object):
    list_display = ['course', 'name','download','add_time']
    search_fields =  ['course', 'name','download' ]
    list_filter =  ['course', 'name','download','add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson  , LessonAdmin)
xadmin.site.register(Video , VideoAdmin)
xadmin.site.register(CourseResource  , CourseResourceAdmin)
xadmin.site.register(BannerCourse  , BannerCourseAdmin)
