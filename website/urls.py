from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    url(r'^studies/$', 'studies.views.home'),
    url(r'^studies/(?P<studynumber>\d+)/$', 'studies.views.data'),
    url(r'^studies/list/$', 'studies.views.list'),
    url(r'^studies/submitted/$', 'studies.view.thanks'),

   )
