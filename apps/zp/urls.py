from django.urls import path

app_name = "zp"

from .api import api

urlpatterns = [
    path("api/", api.urls),
]
