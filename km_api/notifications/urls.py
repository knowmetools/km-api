from django.conf.urls import url


from notifications import views


app_name = 'notifications'


urlpatterns = [
    url(
        r'^devices/apns/$',
        views.APNSDeviceListView.as_view(),
        name='apns-device-list',
    ),
]
