from django.conf.urls import url
from chat import views

urlpatterns = [
    url(r'^groups$', views.GroupView.as_view(), name='list_groups'),
    url(r'^group/new$', views.GroupView.as_view(), name='new_group'),
    url(r'^group/delete/(?P<group_id>[0-9]+)$', views.delete_group, name='delete_group'),
    url(r'^groups/join/(?P<group_id>[0-9]+)$', views.join_group, name='join_group'),
    url(r'^post/list/(?P<group_id>[0-9]+)$', views.GroupChat.as_view(), name='group_chat'),
    url(r'^post/delete/(?P<post_id>[0-9]+)$', views.delete_post, name='erase_post'),
]
