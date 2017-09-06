from django.contrib import admin
from .models import Student,Result,Exam,Courses,Faculty,global_var,Total_Marks#,Grade

from django.contrib.auth.models import Group, User

admin.site.unregister(Group)
#admin.site.unregister(User)
class courseAdmin(admin.ModelAdmin):
     model= Courses
     filter_horizontal = ('students',) 

admin.site.register(Courses, courseAdmin)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(global_var)
admin.site.register(Exam)
