from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

from multiselectfield import MultiSelectField

# Create your models here.
class ParticipantType(models.Model):
    type=models.CharField(max_length=100)

    def __str__(self):
        return self.type
    


class Participant(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(max_length=225)
    designation=models.CharField(max_length=100)
    organization=models.CharField(max_length=200)
    photo=models.ImageField(upload_to='images')
    ph_no=models.CharField(max_length=12)
    gender=models.CharField(max_length=10,null=False)
    participant_type=models.ForeignKey(ParticipantType,on_delete=models.CASCADE)

    created_on=models.DateTimeField(auto_now_add=True)
    created_by=models.CharField(default=name,max_length=100 ,editable=False)
    modified_on=models.DateTimeField(auto_now_add=True)
    modified_by=models.CharField(default=name,max_length=100,editable=False)
    Rstatus=models.CharField(default="v",max_length=1)


    def __str__(self):
        return self.name


class Event(models.Model):

    gender_choice=(
        ('male',"male"),
        ('female','female'),
        ('others','others'),
        ('all','all')
    )
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=500)
    from_date=models.DateField()
    to_date=models.DateField()
    targetted_audience=models.ManyToManyField(ParticipantType)
    gender_specific=models.CharField(max_length=20,choices=gender_choice,default='all')
    event_image=models.ImageField(upload_to='eventimages/')
    topic=models.TextField(max_length=500)
    venue=models.TextField(max_length=200)
    registration_fees=models.FloatField(default='Free')
    paper_submited=models.BooleanField(default=False)
    poster_submited=models.BooleanField(default=False)
    context=models.BooleanField(default=False)   

    
class PaperSubmition(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    papername=models.CharField(max_length=200)
    abstract=models.CharField(max_length=200)
    paperfile=models.FileField(upload_to='uploads/',validators=[FileExtensionValidator( ['pdf'] )])
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,default='pending')
    submit_count=models.IntegerField(default=0)
    remark=models.TextField(max_length=1000,null=True,blank=True)
    camera_ready_submition=models.FileField(upload_to='camera_ready_submitions/',validators=[FileExtensionValidator( ['pdf'] )],null=True,blank=True)
    camera_ready_submition_status=models.CharField(max_length=50,default='active')

    
    

class PosterSubmition(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    postername=models.CharField(max_length=200)
    posterabstract=models.CharField(max_length=200)
    posterfile=models.FileField(upload_to='uploads/',validators=[FileExtensionValidator( ['pdf'] )])
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,default='pending')
    submit_count=models.IntegerField(default=0)
    posterremark=models.TextField(max_length=1000,null=True,blank=True)
    camera_ready_submition=models.FileField(upload_to='camera_ready_submitions/',validators=[FileExtensionValidator( ['pdf'] )],null=True,blank=True)
    camera_ready_submition_status=models.CharField(max_length=50,default='active')

class ContextSubmition(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    contextfile=models.FileField(upload_to='uploads/',validators=[FileExtensionValidator( ['pdf'] )])
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,default='pending')
    submit_count=models.IntegerField(default=0)
    remark=models.TextField(max_length=1000,null=True,blank=True)
    camera_ready_submition=models.FileField(upload_to='camera_ready_submitions/',validators=[FileExtensionValidator( ['pdf'] )],null=True,blank=True)
    camera_ready_submition_status=models.CharField(max_length=50,default='active')

class Privillage(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    participant=models.BooleanField(default=False)
    is_author=models.BooleanField(default=False)
    is_reviewer=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)

    


class User_Event(models.Model):
    event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    registered_date=models.DateTimeField(auto_now_add=True)
    paper=models.BooleanField(default=False)
    poster=models.BooleanField(default=False)
    context=models.BooleanField(default=False)



    
class Reviewer_Paper(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    papername=models.ForeignKey(PaperSubmition,on_delete=models.CASCADE,unique=True)

class Reviewer_Poster(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    postername=models.ForeignKey(PosterSubmition,on_delete=models.CASCADE,unique=True)


class Reviewer_Context(models.Model):
    userid=models.ForeignKey(User,on_delete=models.CASCADE)
    contextname=models.ForeignKey(ContextSubmition,on_delete=models.CASCADE,unique=True)
