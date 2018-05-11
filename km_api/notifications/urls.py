from django.conf.urls import include, url

from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet

from rest_framework.routers import DefaultRouter


app_name = 'notifications'


router = DefaultRouter()
router.register('apns', APNSDeviceAuthorizedViewSet, 'apns-device')


urlpatterns = [
    url(r'^', include(router.urls)),
]
