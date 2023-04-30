from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from prof.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from prof.decorators import *
from django.contrib.auth.models import Group
from prof.models import *
from django.views.generic.edit import UpdateView

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import get_user_model
from datetime import date


from prof.views.sent_mail import sent_mail_from



@unauthenticated_user
def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.filter(username=username).first()
            if user_obj is None:
                messages.success(request, "user not found")
                return redirect("/login")
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.success(request, "wrong password")
                return redirect("/login")

            participant_obj = Participant.objects.filter(user=user).first()
            print(participant_obj)
            if participant_obj != None and participant_obj.Rstatus == "D":
                messages.success(request, "account deactivated")
                return redirect("/login")

            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                previllage = Privillage.objects.filter(userid=user).first()
                print(previllage)
                
                if participant_obj is None and previllage is None:
                    return redirect("/register2")
                
                elif previllage.is_reviewer:
                    return redirect("reviewertable")
                elif previllage.is_admin:
                    return redirect("admin_page")
                else:
                    return redirect("dashboard")
        except Exception as e:
            return HttpResponse("something went wrong")

    return render(request, "base/login.html")




@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            try:
                username = form.cleaned_data.get("username")
                to_email = form.cleaned_data.get("email")
                print(username,to_email)
                if User.objects.filter(username=username).first():
                    messages.success(request, "username taken")
                    return redirect("/register")
                if User.objects.filter(email=to_email).first():
                    messages.success(request, "email taken.")
                    return redirect("/register")

                user = form.save(commit=False)
                user.is_active = False
                user = form.save()

                # print(user)
                # group=Group.objects.get(name='user')
                # user.groups.add(group)
                uid = user.pk
                subject = "your account need to be verified"
                message = f"hi press the link to verify http://127.0.0.1:8000/verify/{uid}"
                
                sent_mail_from(to_email,subject,message)
                messages.success(request, "email has sent.")
                return redirect("/register")
                # login(request, user)
                # return redirect('register2')
            except Exception as e:
                return HttpResponse("something went wrong")
        else:
            messages.error(request, form.error_messages)
    context = {"form": form}
    return render(request, "base/registration.html", context)


def token_sent(request):
    return render(request, "base/token.html")


def verify(request, uid):
    User = get_user_model()

    user = User.objects.get(pk=uid)

    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("register2")

    else:
        return HttpResponse("Activation link is invalid!")


def register2(request):
    form2 = Registration2Form()
    if request.method == "POST":
        form2 = Registration2Form(request.POST, request.FILES)
        if form2.is_valid():
            participant = form2.save(commit=False)
            participant.user = request.user
            #   print(participant)
            participant.save()
            privillage = Privillage()
            privillage.userid = request.user
            privillage.participant = True
            privillage.save()
            return redirect("dashboard")

    return render(request, "base/registration2.html", {"form2": form2})



def logoutpage(request):
    logout(request)
    return redirect("login")
