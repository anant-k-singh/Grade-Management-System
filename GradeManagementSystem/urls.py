from django.conf.urls import url
from django.contrib import admin
from gms.views import log_in,log_out,authenticated,course,addexam,setcriteria,update_exam

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$',log_in,name='log_in'),
    url(r'^$',log_in,name='log_in'),
    url(r'^logout/$',log_out,name='log_out'),
    url(r'^authenticated/$',authenticated,name='authenticated'),
    url(r'^authenticated/(?P<course_no>[0-9]+)/$',course,name='course'),
    url(r'^authenticated/(?P<course_no>[0-9]+)/addexam/$',addexam,name='addexam'),
    url(r'^authenticated/(?P<course_no>[0-9]+)/setcriteria/$',setcriteria,name='setcriteria'),
    url(r'^authenticated/(?P<course_no>[0-9]+)/(?P<exam_no>[0-9]+)/$',update_exam,name='update_exam'),

]
