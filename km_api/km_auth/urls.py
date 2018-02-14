"""URLs for authentication views.
"""

from django.conf.urls import url

from km_auth import views


urlpatterns = (
    url(r'^layer/$', views.LayerIdentityView.as_view(), name='layer'),
    url(r'^login/$', views.ObtainTokenView.as_view(), name='login'),
)
