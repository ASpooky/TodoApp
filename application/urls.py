from django.urls import path
from . import views

app_name="application"

urlpatterns=[
    path("",views.indexView.as_view(),name="index"),
    path("regist/",views.registView.as_view(),name="regist"),
]