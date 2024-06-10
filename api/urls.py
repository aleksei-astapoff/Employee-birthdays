from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import BirthdaysViewSet, UserViewSet

app_name = 'api'


router_v1 = DefaultRouter()


router_v1.register('users', viewset=UserViewSet, basename='users')

router_v1.register('birthdays', viewset=BirthdaysViewSet, basename='birthdays')

urlpatterns = [
    path('', include(router_v1.urls)),
]
