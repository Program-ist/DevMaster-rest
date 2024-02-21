from django.db import models

# Create your models here.

class UserDetail(models.Model):
    name = models.CharField(max_length=200)
    user_name = models.CharField(max_length=200)    
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    status_of_account = models.CharField(max_length=200)



    def __str__(self):
        return self.name
    
