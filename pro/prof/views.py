from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .models import *
from django.views.generic.edit import UpdateView
from django.core.mail import send_mail
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import get_user_model
# Create your views here.

def index(request):
    return render(request,'main.html')

@unauthenticated_user
def register(request):
    
    

        form=CreateUserForm()
        
        if request.method == "POST":
            
            form=CreateUserForm(request.POST)
        
            if form.is_valid():
                try:
                    username=form.cleaned_data.get('username')
                    to_email=form.cleaned_data.get('email')
                    if User.objects.filter(username=username).first():
                       messages.success(request, 'username taken')
                       return redirect('/register')
                    if User.objects.filter(email=to_email).first():
                       messages.success(request, 'email taken.')
                       return redirect('/register')

                    user=form.save(commit=False)
                    user.is_active=False
                    user=form.save()

                    # print(user)
                    # group=Group.objects.get(name='user')
                    # user.groups.add(group)
                    
                    sent_mail_from(to_email,user)
                    return redirect('token_sent')
                    # login(request, user)
                    # return redirect('register2')
                except Exception as e:
                     return HttpResponse("something went wrong")
        context={'form':form}
        return render(request,'registration.html',context)


def token_sent(request):
      return render(request,'token.html')


def verify(request,uid):
    User = get_user_model()

    user=User.objects.get(pk=uid)

    if user is not None:
        user.is_active=True
        user.save()
        login(request, user)
        return redirect('register2')
        
    else:  
        return HttpResponse('Activation link is invalid!')  
    
      
      
def register2(request):
    form2=Registration2Form()
    if request.method =="POST":
            papersubmition=request.POST.get('papersubmition')
            print(papersubmition)
            form2=Registration2Form(request.POST,request.FILES)
            if form2.is_valid():
                
                  
                  participant=form2.save(commit=False)
                  participant.user = request.user
                #   print(participant)
                  participant.save()
                  if papersubmition == 'True' :
                       return redirect('papersubmition')
                  else:
                       
                       return redirect('/')
    
    return render(request,'registration2.html',{'form2':form2})
            
      
def papersubmition(request):
     form=PaperSubmitionForm()

     if request.method =='POST':
          form=PaperSubmitionForm(request.POST,request.FILES)
          if form.is_valid():
               papersubmition=form.save(commit=False)
               papersubmition.userid=request.user
               papersubmition.save()
               return redirect('/') 
     return render(request,'papersubmition.html',{'form':form})  





def Editprofile(request):
    
     user=request.user
    
     participant_obj=Participant.objects.get(user=user)
     papersubmition_obj=PaperSubmition.objects.get(userid=user)
     print(participant_obj)
     
     if request.method =="POST":
            form=EditForm(request.POST,request.FILES,instance=participant_obj)
            papereditform=EditPaperSubmitionForm(request.POST,request.FILES,instance=papersubmition_obj)
            if form.is_valid() and papereditform.is_valid():
                  participant=form.save(commit=False)
                  
                  participant.save()
                  papersubmition=papereditform.save(commit=False)
                  papersubmition.save()
                  return redirect('settings')
     form=EditForm(instance=participant_obj)
     papereditform=EditPaperSubmitionForm(instance=papersubmition_obj)
     return render(request,'profile.html',{'form':form,'participant_obj':participant_obj,'form2':papereditform,'papersubmition_obj':papersubmition_obj})




@unauthenticated_user
def loginpage(request):
    
 

        if request.method == "POST":
            username=request.POST.get('username')
            password=request.POST.get('password')

            try:
                 
                user_obj=User.objects.filter(username=username).first()
                if user_obj is None:
                    messages.success(request, 'user not found')
                    return redirect('/login')
                user= authenticate(request,username=username,password=password)
                if user is None:
                    messages.success(request, 'wrong password')
                    return redirect('/login')
                
                participant_obj=Participant.objects.get(user=user)
                if participant_obj.Rstatus=='D':
                    messages.success(request, 'account deactivated')
                    return redirect('/login')
                    
                user = authenticate(request,username=username,password=password)
                if user is not None:

                        login(request,user)
                        return redirect('/')
            except Exception as e:
                 return HttpResponse("something went wrong")

        return render(request,'login.html')




def logoutpage(request):
    logout(request)
    return redirect('login')




def sent_mail_from(email,user):
    print(user.pk)
    print(user.id)
    uid=user.pk
    subject="your account need to be verified"
    message=f'hi press the link to verify http://127.0.0.1:8000/verify/{uid}'
    email_from=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail( subject, message, email_from, recipient_list )


