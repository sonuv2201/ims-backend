from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HomeView


router = DefaultRouter()

router.register(r"home", HomeView, basename="home")

urlpatterns = router.urls
