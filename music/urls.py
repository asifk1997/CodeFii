from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<problemset_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<problemset_id>[0-9]+)/(?P<problem_id>[0-9]+)/$', views.problemdetail, name='problemdetail'),
    url(r'^(?P<problemset_id>[0-9]+)/(?P<problem_id>[0-9]+)/(?P<submission_id>[0-9]+)/$', views.solution_verdict, name='solution_verdict'),
    url(r'^(?P<problem_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^problems/(?P<filter_by>[a-zA_Z]+)/$', views.problems, name='problems'),
    url(r'^create_problemset/$', views.create_problemset, name='create_problemset'),
    url(r'^(?P<problemset_id>[0-9]+)/create_problem/$', views.create_problem, name='create_problem'),
    url(r'^(?P<problemset_id>[0-9]+)/delete_problem/(?P<problem_id>[0-9]+)/$', views.delete_problem, name='delete_problem'),
    url(r'^(?P<problemset_id>[0-9]+)/favorite_problemset/$', views.favorite_problemset, name='favorite_problemset'),
    url(r'^(?P<problemset_id>[0-9]+)/delete_problemset/$', views.delete_problemset, name='delete_problemset'),
]
