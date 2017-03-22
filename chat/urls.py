from django.conf.urls import url
from chat import views

urlpatterns = [
    url(r'^groups$', views.ListGroups.as_view(), name='list_groups'),
]
