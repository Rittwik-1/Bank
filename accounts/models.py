from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password= None, ):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(
            email = self.normalize_email(email),
              )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using = self.db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None,):
        if not email:
            raise ValueError('Email is Required')
        user = self.create_user(
            email = self.normalize_email(email),
            password=password, first_name =first_name, last_name=last_name
              )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.first_name = first_name
        user.last_name = last_name
        user.save(using = self.db)
        return user

import uuid
import random

class CustomUser(AbstractUser):

    uuid = models.IntegerField(blank=True,null=True)
    username = None
    first_name = models.CharField(verbose_name='First Name', max_length=100, )
    last_name = models.CharField(verbose_name='Last Name', max_length=100, )
    email = models.EmailField(db_index=True, unique=True,)
    
    credit_card = models.IntegerField(null=True,default=None,blank=True)
    
    
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name' ]
    EMAIL_FIELD = 'email'


    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.uuid:
                while True:
                    self.uuid =  random.randint(000000000000,999999999999)
                    if not self.__class__.objects.filter(uuid=self.uuid):
                        break
   
        super(CustomUser, self).save(*args, **kwargs)

