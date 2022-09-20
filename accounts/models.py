from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import random



class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password= None, ):

        """
        Creates and saves a User with the given email, first_name, last_name and password.

        """
        if not email:
            raise ValueError('Email is Required')
        user = self.model(
            email = self.normalize_email(email), # normalize_email() is used to convert the email to lowercase
              )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using = self.db) # save the user to the database
        return user


class CustomUser(AbstractUser):
    """
    This is the model for the user
    """
    uuid = models.IntegerField(blank=True,null=True)
    username = None
    
    first_name = models.CharField(verbose_name='First Name', max_length=100)
    last_name = models.CharField(verbose_name='Last Name', max_length=100)
    email = models.EmailField(db_index=True, unique=True)
    credit_card = models.IntegerField(null=True,default=None,blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name' ] # Create your models here.
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.first_name


    """
    This is a method for the user which creates a account_number for the user.
    """
    def save(self, *args, **kwargs):
        if not self.uuid:
                while True:
                    self.uuid =  random.randint(000000000000,999999999999)
                    if not self.__class__.objects.filter(uuid=self.uuid):
                        break
   
        super(CustomUser, self).save(*args, **kwargs)

