from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'cabUserAuth'
urlpatterns = [
    url(r'^user/register', views.register_user)
]

urlpatterns = format_suffix_patterns(urlpatterns)