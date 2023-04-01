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

class EditPaperSubmitionForm(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['papername','abstract','paperfile']

class EditPosterSubmitionForm(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['postername','posterabstract','posterfile']

class EditPosterSubmitionFormReviewer(ModelForm):
    class Meta:
        model=PosterSubmition
        fields=['status','posterremark']

class EditPaperrSubmitionFormReviewer(ModelForm):
    class Meta:
        model=PaperSubmition
        fields=['status','remark']



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

