"""km_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from rest_framework.documentation import include_docs_urls


urlpatterns = [
    url(r"^account/", include("rest_email_auth.urls")),
    url(r"^account/", include("account.urls")),
    url(r"^admin/", admin.site.urls),
    url(
        r"^api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    path("apple/", include("apple.urls")),
    url(r"^auth/", include("km_auth.urls")),
    url(r"^docs/", include_docs_urls(title="Know Me API")),
    url(r"^know-me/", include("know_me.urls")),
    url(r"^status/", include("status.urls")),
]
