from django.db import models
from django.contrib.auth.models  import (PermissionsMixin, BaseUserManager, AbstractBaseUser)  
from django.contrib.auth.validators  import UnicodeUsernameValidator  
import jwt
from django.conf import settings
from datetime import datetime,timedelta
# Create your models here.
class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ('-created_at',)
        
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        # if not name:
        #     raise ValueError('Users must have a  name')

        
        user = self.model(
            email=email.lower())
            # name=name        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=email.lower(),
            password=password
            # name=name
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_pro = True
        
        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    objects = MyUserManager()
    @property
    def tokens(self):
        token = jwt.encode({'email': self.email, 'id': self.id, 'exp':datetime.utcnow() + timedelta(hours=24)},settings.SECRET_KEY, algorithm='HS256')
        return token
        
    def __str__(self):
        return self.email
