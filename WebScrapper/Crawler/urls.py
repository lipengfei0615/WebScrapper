from django.conf.urls import url

from Crawler.views import MyView,AthletesListView,AthletesDetailsView,RecordListView,RecordDetailView,CalenderView,RankingView,MeetView,MeetDetailView,EmailView

app_name = 'Crawler'
urlpatterns = [
    url(r'^home/$', MyView.as_view(), name='home'),
    url(r'^athletes/$', AthletesListView.as_view(), name='athletes'),
    url(r'^athletesSearch/$', AthletesListView.as_view(), name='athletesSearch'),
    url(r'^athletes/(?P<athletes_id>\d+)$', AthletesDetailsView.as_view(), name='personal_best'),
    url(r'^recordlist/$', RecordListView.as_view(), name='recordlist'),
    url(r'^recordlist/(?P<id>\d+)$', RecordDetailView.as_view(), name='record'),
    url(r'^calender/$', CalenderView.as_view(), name='calender'),
    url(r'^ranking/$', RankingView.as_view(), name='ranking'),
    url(r'^rankingcondition/$', RankingView.as_view(), name='rankingcondition'),
    url(r'^meet/$', MeetView.as_view(), name='meet'),
    url(r'^meetfilter/$', MeetView.as_view(), name='meetfilter'),
    url(r'^meet/(?P<meets_id>\d+)$', MeetDetailView.as_view(), name='medal'),
    url(r'^contact/$', EmailView.as_view(), name='email'),
]