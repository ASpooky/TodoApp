from django.urls import path
from . import views

app_name="application"

urlpatterns=[
    path("",views.indexView.as_view(),name="index"),
    path("regist/",views.registView.as_view(),name="regist"),
    path("login/",views.LoginView.as_view(),name="login"),
    path("target_list/",views.TargetListView.as_view(),name="target_list"),
    path("target_list/<str:day>/",views.TargetRegistView.as_view(),name="target_regist"),
    path("target_update/",views.get_update_target,name="get_update_target"),
    path("target_update/<int:pk>",views.TargetUpdateView.as_view(),name="target_update"),
    path("target_delete/<int:pk>",views.TargetDeleteView.as_view(),name="target_delete"),
    #path("target_update/<str:update>",views.TargetUpdateView.as_view(),name="target_update"),
    #path("target_regist/",views.TargetRegistView.as_view(),name="target_regist"),
    path("target_get/",views.get_targets,name="target_get"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
]