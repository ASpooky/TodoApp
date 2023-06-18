import os

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView,FormView
from .form import RegistForm


# Create your views here.

class indexView(TemplateView):
    template_name=os.path.join("application","index.html")

class registView(CreateView):
    template_name=os.path.join("application","regist.html")
    form_class=RegistForm

    success_url=reverse_lazy("application:index")