import os
import json
import time
import datetime
from typing import Any, Dict
from django import http

from django.utils import timezone

from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,FormView,UpdateView,DeleteView
)
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse,Http404
from django.contrib import messages

from .form import (
    UserRegistForm,LoginForm,TargetRegistForm,TargetUpdateForm,
)
from .models import Target


# Create your views here.

class indexView(TemplateView):
    template_name=os.path.join("application","index.html")

class registView(CreateView):
    template_name=os.path.join("application","regist.html")
    form_class=UserRegistForm

    success_url=reverse_lazy("application:index")

class LoginView(FormView):
    template_name=os.path.join("application","login.html")
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        email=request.POST["email"]
        password=request.POST["password"]
        user=authenticate(email=email,password=password)
        next_url=request.POST["next"]
        if user is not None and user.is_active:
            login(request,user)
            if next_url:
                return redirect(next_url)
            return redirect("application:index")
        else:
            form.add_error(None, 'メールアドレス、またはPASSWORDが違います。')
            return render(request,"application/login.html",{'form': form})
        
class LogoutView(FormView):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("application:login")
        
class TargetListView(LoginRequiredMixin,TemplateView):
    template_name=os.path.join("application","target_list.html")

class TargetRegistView(LoginRequiredMixin,CreateView):
    template_name=os.path.join("application","target_regist.html")
    form_class=TargetRegistForm

    def post(self,request,*args,**kwargs):
        form=TargetRegistForm(request.POST)
        title=request.POST.get("title")
        memo=request.POST.get("memo")
        start=request.POST["start"]
        deadline=request.POST["deadline"]
        user=request.user
        target=Target(user=user,title=title,memo=memo,start=start,deadline=deadline)
        if title is not None:
            target.save()
        else:
            return render(request,"application/target_regist.html",{'form': form})
        return redirect("application:target_list")

    success_url=reverse_lazy("application:target_list")

class TargetUpdateView(LoginRequiredMixin,UpdateView):
    template_name=os.path.join("application","target_update.html")
    form_class=TargetUpdateForm
    model=Target
    success_url=reverse_lazy("application:target_list")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context["pk"]=context["target"].id
        return context#ここを変更してhtmlでpkを受け取れるようにする

class TargetDeleteView(LoginRequiredMixin,DeleteView):
    template_name=os.path.join("application","target_delete.html")
    model=Target
    success_url=reverse_lazy("application:target_list")
    

def target_regist(request):
    return render(request,"application/regist.html")

def get_targets(request):

    if request.method=="GET":
        return Http404()
    
    datas = json.loads(request.body)
    
    start=datas["start_date"]
    deadline=datas["end_date"]

    user=request.user

    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(deadline / 1000))

    target=Target.objects.filter(
        start__lt=formatted_end_date,deadline__gt=formatted_start_date,user=user
    )

    list = []
    for t in target:
        color="grey" if t.clear else "rgb(83, 187, 195)"
        list.append(
            {
            "title": t.title,
            "start": t.start,
            "end": t.deadline,
            "clear":t.clear,
            "color":color,
            }
        )

    return JsonResponse(list,safe=False)

def get_update_target(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form=TargetUpdateForm(request.GET)
        start=int(request.GET.get("start"))
        title=request.GET.get("title")

        user=request.user

        formatted_start_date = time.strftime(
            "%Y-%m-%d", time.localtime(start / 1000))

        target=Target.objects.filter(
            start=formatted_start_date,user=user,title=title
        )

        t=target.first()

        return redirect("application:target_update",pk=t.id)
