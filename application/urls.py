from django.urls import path
from . import views

app_name="application"

urlpatterns=[
    path("",views.indexView.as_view(),name="index"),
    path("regist/",views.registView.as_view(),name="regist"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("target_list/",views.TargetListView.as_view(),name="target_list"),
    path("target_list/<str:day>/",views.TargetRegistView.as_view(),name="target_regist"),
    #path("target_regist/",views.TargetRegistView.as_view(),name="target_regist"),
    path("target_get/",views.get_targets,name="target_get"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
]