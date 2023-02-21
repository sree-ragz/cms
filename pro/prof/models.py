from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Participant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=225)
    designation=models.CharField(max_length=100)
    organization=models.CharField(max_length=200)
    photo=models.ImageField(upload_to='images')
    ph_no=models.CharField(max_length=12)
    is_author=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)
    created_by=models.CharField(default=name,max_length=100 ,editable=False)
    modified_on=models.DateTimeField(auto_now_add=True)
    modified_by=models.CharField(default=name,max_length=100,editable=False)
    Rstatus=models.CharField(default="v",max_length=1)


    def __str__(self):
        return self.name
    
    
   