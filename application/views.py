import os
import json
import time

from django.utils import timezone

from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,FormView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse,Http404

from .form import UserRegistForm,LoginForm,TargetRegistForm
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

    success_url=reverse_lazy("application:target_list")

def target_regist(request):
    return render(request,"application/regist.html")

def get_targets(request):

    if request.method=="GET":
        return Http404()
    
    datas = json.loads(request.body)
    
    start=datas["start_date"]
    deadline=datas["end_date"]

    formatted_start_date = time.strftime(
        "%Y-%m-%d", time.localtime(start / 1000))
    formatted_end_date = time.strftime(
        "%Y-%m-%d", time.localtime(deadline / 1000))

    target=Target.objects.filter(
        start__lt=formatted_end_date,deadline__gt=formatted_start_date
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