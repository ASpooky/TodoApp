from django import forms
from .models import Users,Target
from django.contrib.auth.password_validation import validate_password
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
    title=forms.CharField(label="目標",max_length=150)
    d_today=datetime.date.today()
    memo=forms.CharField(label="メモ",max_length=300)
    start=forms.DateField(label="始めた日",initial=d_today,widget=DateInput())
    deadline=forms.DateField(label="終了予定",initial=d_today,widget=DateInput())

    class Meta:
        model=Target
        fields=["title","memo","start","deadline"]

