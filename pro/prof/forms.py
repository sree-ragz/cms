from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, widgets
from .models import *



class DateInput(forms.DateInput):
    input_type='date'


class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class CreateChairAndCochairForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class Registration2Form(ModelForm):
    class Meta:
        model=Participant
        fields=['name','email','designation','organization','photo','ph_no','gender','participant_type']



class EditForm(ModelForm):
    class Meta:
        model=Participant
        fields=['name','email','designation','organization','photo','ph_no','participant_type']


class PaperSubmitionForm(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['papername','abstract','paperfile']

class PosterSubmitionForm(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['postername','posterabstract','posterfile']

class ContextSubmitionForm(ModelForm):
    class Meta:
        model=ContextSubmition
        fields=['name','contextfile']

class EditPaperSubmitionForm(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['papername','abstract','paperfile']

class EditPosterSubmitionForm(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['postername','posterabstract','posterfile']
class EditContextSubmitionForm(ModelForm):
    class Meta:
        model=ContextSubmition
        fields=['name','contextfile']


class CameraReadyPaperSubmitionForm(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['camera_ready_submition']
class CameraReadyPosterSubmitionForm(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['camera_ready_submition']
class CameraReadyContextSubmitionForm(ModelForm):
    class Meta:
        model=ContextSubmition
        fields=['camera_ready_submition']
class EditPosterSubmitionFormReviewer(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['status','posterremark','camera_ready_submition_status','admin_remark']
class EditCameraReadyPaperSubmitionFormReviewer(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['camera_ready_submition_status']
class EditCameraReadyPosterSubmitionFormReviewer(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['camera_ready_submition_status']
class EditCameraReadyContextSubmitionFormReviewer(ModelForm):
    class Meta:
        model=ContextSubmition
        fields=['camera_ready_submition_status']
class EditPaperrSubmitionFormReviewer(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['status','remark']
class EditPaperrSubmitionFormAdmin(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['status','camera_ready_submition_status','admin_remark']

class EditContextSubmitionFormReviewer(ModelForm):
    class Meta:
        model=ContextSubmition
        fields=['status','remark','camera_ready_submition_status','admin_remark']



class PaperReviewForm(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['paperfile','remark']


class PosterReviewForm(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['posterfile','posterremark']

class AdminAddorEditEvent(ModelForm):
    class Meta:
        model=Event
        fields='__all__'

        widgets={

            'from_date':DateInput(),
            'to_date':DateInput()
        }


class AdminAddorEditReviewerPaper(ModelForm):
    class Meta:
        model=Reviewer_Paper
        fields='__all__'

        widgets={

            'from_date':DateInput(),
            'to_date':DateInput()
        }

class AdminAddorEditReviewerPoster(ModelForm):
    class Meta:
        model=Reviewer_Poster
        fields='__all__'

        widgets={

            'from_date':DateInput(),
            'to_date':DateInput()
        }

class AdminAddorEditReviewerContext(ModelForm):
    class Meta:
        model=Reviewer_Context
        fields='__all__'

        widgets={

            'from_date':DateInput(),
            'to_date':DateInput()
        }


class AdminUser(ModelForm):
    class Meta:
        model=Participant
        fields=["Rstatus"]
        
