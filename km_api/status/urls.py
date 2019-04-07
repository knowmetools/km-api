from django.urls import path

from status import views

app_name = "status"


urlpatterns = [path("", views.health_check, name="status")]
