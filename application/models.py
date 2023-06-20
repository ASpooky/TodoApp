from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser,PermissionsMixin,BaseUserManager
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError(" Enter Email ")
        
        user=self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=150)
    email=models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects=UserManager()

    class Meta:
        db_table="users"

class Target(models.Model):
    title=models.CharField(max_length=150)
    memo=models.TextField()
    start=models.DateField(default=timezone.now)
    deadline=models.DateField(default=timezone.now)
    clear=models.BooleanField(default=False)

    class Meta:
        db_table="target"
