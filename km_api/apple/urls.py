from django.urls import path

from apple import views


app_name = "apple"


urlpatterns = [
    path(
        "receipt-type-query/",
        views.ReceiptTypeQueryView.as_view(),
        name="receipt-type-query",
    )
]
