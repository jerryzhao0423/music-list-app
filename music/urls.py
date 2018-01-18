from django.urls import path, re_path
from django.conf.urls import url
from . import views

app_name = 'music'
urlpatterns = [
    path('', views.index, name='index'),
    url('^songs/$', views.song_detail, name='songs'),
    url('^register/$', views.UserFormView.as_view(), name='register'),
    url('^login/$', views.login_user, name='login'),
    url('^logout/$', views.login_user, name='logout'),
    url('^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    path('album/add/', views.create_album, name='album_add'),
    url('album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album_delete'),
    url('album/(?P<pk>[0-9]+)/create_song/$', views.create_song, name='song_add'),
    url('album/(?P<pk>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='song_delete'),
]
