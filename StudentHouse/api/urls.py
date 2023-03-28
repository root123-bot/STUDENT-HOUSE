from StudentHouse.register.views import *
from django.conf.urls import url
from django.urls import path
from StudentHouse.user.views import *
from StudentHouse.organization.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    url(r'completeteacherprofile/$', teacher_profile, name="teacher_complete"),
    url(r'admin_addteacher/$', admin_addteacher, name="admin_addteacher"),
    url(r'userdetail/$', user_details, name="userdetails"),
    url(r'register/$', register, name="register"),
    url(r'token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
]
