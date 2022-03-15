
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'newsitems', views.NewsitemViewSet)
router.register(r'keys',views.KeyViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'postingsites',views.PostingsiteViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
