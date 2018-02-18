"""URLs for authentication views.
"""

from django.conf.urls import url

from km_auth import views


urlpatterns = (
    url(r'^login/$', views.ObtainTokenView.as_view(), name='login'),
)
