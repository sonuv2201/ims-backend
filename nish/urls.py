"""
URL configuration for nish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from generic.views import (
    ChangePasswordViewset,
    CustomTokenRefreshView,
    HomePageView,
    ResetPasswordViewset,
)

from nish import settings
from superadmin.views import LCNCManagementViewSet, AuthConfigurationViewSet

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from generic.views import CustomTokenObtainPairView

from rest_framework.routers import DefaultRouter

from django.contrib import admin

from django.views.static import serve
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_header = "J Q National Distributors Admin"  # default: "Django Administration"
admin.site.index_title = "J Q National Distributors Features"  # default: "Site administration"
admin.site.site_title = "J Q National Distributors Admin"  # default: "Django site admin"

urlpatterns = [
    path(
        "", HomePageView.as_view(), name="home"
    ),  # This routes the root URL (/) to the DRF view
    #path("admin/", admin.site.urls, name="admin"), 
    #path("api/", include("homerun.urls")),
    path("api/", include("ims.urls")),
    path('admin/', admin.site.urls),
    path("api/", include("superadmin.urls")),
    path("generic-api/", include("generic.urls")),
    path("api/refresh-token/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    re_path(
        r"^lcnc-frontend/public/assets/(?P<path>.*)$",
        serve,
        {
            "document_root": "lcnc-frontend/public/assets",
        },
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

router = DefaultRouter()
router.register(
    r"auth/configuration", AuthConfigurationViewSet, basename="auth_configuration"
)
router.register(
    r"noauth/api/login-via-email/password",
    CustomTokenObtainPairView,
    basename="token_obtain_pair",
)

router.register(
    r"noauth/api/reset/password/email",
    ResetPasswordViewset,
    basename="reset_password",
)

router.register(
    r"noauth/api/reset/password/email/otp",
    ChangePasswordViewset,
    basename="change_password",
)

router.register(r"lcnc-management", LCNCManagementViewSet, basename="lcnc_management")


urlpatterns += router.urls
