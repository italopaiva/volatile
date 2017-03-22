from django.conf.urls import url
from chat import views

urlpatterns = [
    url(r'^groups$', views.ListGroups.as_view(), name='list_groups'),
    url(r'^groups/join/(?P<group_id>[0-9]+)$', views.join_group, name='join_group'),
]
