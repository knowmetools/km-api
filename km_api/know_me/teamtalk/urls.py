"""URLs for the ``know_me.teamtalk`` module.
"""

from django.conf.urls import url

from know_me.teamtalk import views


urlpatterns = [
    url(r'^authenticate/$', views.LayerIdentityView.as_view(), name='authenticate'),    # noqa
]
