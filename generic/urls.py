from django.urls import path, reverse, NoReverseMatch
from rest_framework.routers import DefaultRouter
from .views import (
    GroupingEntityPermissionsViewSet,
    GroupingViewSet,
    EntityViewSet,
    UserViewSet,
    GroupViewSet,
)
from generic import views

router = DefaultRouter()
router.register(r"entities", EntityViewSet, basename="entity")
router.register(r"users", UserViewSet, basename="user")
# router.register(r"groups", GroupViewSet, basename="group")
router.register(r"groups", GroupingViewSet, basename="Group")
router.register(
    r"groups-entity-permissions",
    GroupingEntityPermissionsViewSet,
    basename="Group-entity-permissions",
)
router.register(r"groups-user", views.GroupUserViewSet)
# router.register(r"admin-menus", views.AdminMenuViewSet)
router.register(
    r"entities-permission",
    views.EntityPermissionViewset,
    basename="entities-permission",
)
router.register(r"access-control", views.AccessControlViewSet)

# Fetch all registered routes


# Generate the route list
urlpatterns = router.urls
