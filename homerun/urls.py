from rest_framework.routers import DefaultRouter


from homerun.views import BookViewSet

router = DefaultRouter()

router.register(r"book", BookViewSet, basename="book")


urlpatterns = router.urls
