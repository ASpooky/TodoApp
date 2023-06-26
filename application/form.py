from typing import Any, Dict
from django import forms
from .models import Users,Target
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
import datetime

class DateInput(forms.DateInput):
    input_type="date"

class UserRegistForm(forms.ModelForm):
    username=forms.CharField(label="名前")
    email=forms.EmailField(label="メールアドレス")
    password=forms.CharField(label="パスワード",widget=forms.PasswordInput())
    confirm_password=forms.CharField(label="パスワード再入力",widget=forms.PasswordInput())

    class Meta:
        model=Users
        fields=["username","email","password","confirm_password"]

    
    def save(self):
        user=super().save(commit=False)
        validate_password(self.cleaned_data["password"],user)
        user.set_password(self.cleaned_data["password"])
        user.save()
        return user
    
class LoginForm(forms.Form):
    email=forms.EmailField(label="メールアドレス")
    password=forms.CharField(label="パスワード",widget=forms.PasswordInput())

class TargetRegistForm(forms.ModelForm):
    title=forms.CharField(label="目標",max_length=150,error_messages={'required': '予定や目標を自由に登録しよう'})
    d_today=datetime.date.today()
    memo=forms.CharField(label="メモ",max_length=300,required=False)
    start=forms.DateField(label="始めた日",initial=d_today,widget=DateInput())
    deadline=forms.DateField(label="終了予定",initial=d_today,widget=DateInput())
    
    class Meta:
        model=Target
        fields=["title","memo","start","deadline"]
        

class TargetUpdateForm(forms.ModelForm):
    
    memo=forms.CharField(label="メモ",max_length=300,required=False)
    clear=forms.BooleanField(initial=False,required=False)
    id=forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model=Target
        fields=["memo","clear","id"]


