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


def dashboard(request):
    events = Event.objects.all()
    print(events)
    user = request.user
    previllage = Privillage.objects.filter(userid=request.user).first()

    participant_obj = Participant.objects.filter(user=user).first()

    return render(
        request,
        "user/dashboard.html",
        {"event": events, "participant": participant_obj, "previllage": previllage,"today": date.today()},
    )


def eventregistration(request, event_id):
    if request.user.is_authenticated:
        previllage = Privillage.objects.filter(userid=request.user).first()
        print(event_id)
        user_events_obj = User_Event.objects.filter(
            event_id=event_id, user_id=request.user
        ).first()
        # print(user_events_obj.poster)

        events = Event.objects.get(pk=event_id)
        print(events)
        print(events.title)
        form = PaperSubmitionForm()
        form2 = PosterSubmitionForm()
        if request.method == "POST":
            form = PaperSubmitionForm(request.POST, request.FILES)
            form2 = PosterSubmitionForm(request.POST, request.FILES)
            if form.is_valid():
                print(request.user)
                privillages = Privillage.objects.get(userid=request.user)
                user_events = User_Event.objects.filter(
                    event_id=event_id, user_id=request.user
                ).first()
                print(privillages.is_author)
                print(user_events)
                if privillages.is_author is False:
                    privillages.is_author = True
                    privillages.save()
                else:
                    privillages.is_author = True
                    privillages.save()

                if user_events is None:
                    user_event = User_Event()
                    user_event.event_id = events
                    user_event.user_id = request.user
                    user_event.paper = True
                    user_event.save()
                else:
                    user_events.paper = True
                    user_events.save()

                papersubmition = form.save(commit=False)
                papersubmition.userid = request.user
                papersubmition.event = events
               #  papersubmition.submit_count = 1
                papersubmition.save()
                obj=PaperSubmition.objects.filter(userid=request.user,event=event_id).first()
                to_email=obj.userid.email
                subject = "your paper has been successfully submitted"
                message = f"your paper has been successfully submitted for {events.title} with paper id {obj.pk}"
                sent_mail_from(to_email,subject,message)
                


            if form2.is_valid():
                privillages = Privillage.objects.filter(userid=request.user).first()
                user_events = User_Event.objects.filter(
                    event_id=event_id, user_id=request.user
                ).first()

                if privillages.is_author is False:
                    privillages.is_author = True
                    privillages.save()
                else:
                    privillages.is_author = True
                    privillages.save()

                if user_events is None:
                    user_event = User_Event()
                    user_event.event_id = events
                    user_event.user_id = request.user
                    user_event.poster = True
                    user_event.save()
                else:
                    user_events.poster = True
                    user_events.save()

                postersubmition = form2.save(commit=False)
                postersubmition.userid = request.user
                postersubmition.event = events
                # postersubmition.submit_count = 1
                postersubmition.save()

                obj=PosterSubmition.objects.filter(userid=request.user,event=event_id).first()
                to_email=obj.userid.email
                subject = "your poster has been successfully submitted"
                message = f"your poster has been successfully submitted for {events.title} with poster id {obj.pk}"
                sent_mail_from(to_email,subject,message)

            return redirect("eventregistration", event_id)

        return render(
            request,
            "user/eventregistration.html",
            {
                "event": events,
                "form": form,
                "form2": form2,
                "userevents": user_events_obj,
                "previllage": previllage,
            },
        )

    else:
        return redirect("login")


def register_as_participant(request, event_id):
    events = Event.objects.get(pk=event_id)
    user_events = User_Event.objects.filter(
        event_id=event_id, user_id=request.user
    ).first()
    print(user_events)

    if user_events is None:
        user_event = User_Event()
        user_event.event_id = events
        user_event.user_id = request.user
        user_event.paper = False
        user_event.poster = False
        user_event.save()
    else:
        user_events.paper = False
        user_events.poster = False
        user_events.save()
    to_email=user_event.user_id.email
    subject = "your are successfully registered as a participant"
    message = f"your are successfully registered as a participant for {events.title}"
    sent_mail_from(to_email,subject,message)
    return redirect("eventregistration", event_id)


def user_context_registration(request,event_id):

    if request.method=='POST':
        events = Event.objects.get(pk=event_id)
        print(events)
        
        
        form=ContextSubmitionForm(request.POST,request.FILES)
        if form.is_valid():
                events = Event.objects.get(pk=event_id)
                privillages = Privillage.objects.filter(userid=request.user).first()
                user_events = User_Event.objects.filter(
                    event_id=event_id, user_id=request.user
                ).first()

                if privillages.is_author is False:
                    privillages.is_author = True
                    privillages.save()
                else:
                    privillages.is_author = True
                    privillages.save()

                if user_events is None:
                    user_event = User_Event()
                    user_event.event_id = events
                    user_event.user_id = request.user
                    user_event.context = True
                    user_event.save()
                else:
                    user_events.context = True
                    user_events.save()
                
                context = form.save(commit=False)
                context.userid = request.user
                context.event = events
               
                context.save()
                obj=ContextSubmition.objects.filter(userid=request.user,event=event_id).first()
                to_email=obj.userid.email
                subject = "your context has been successfully submitted"
                message = f"your context has been successfully submitted for {events.title} with context id {obj.pk}"
                sent_mail_from(to_email,subject,message)

        return redirect("eventregistration", event_id)
        

    

def Editprofile(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    user = request.user

    participant_obj = Participant.objects.filter(user=user).first()

   
    print(participant_obj)

    if request.method == "POST":
        form = EditForm(request.POST, request.FILES, instance=participant_obj)
        
        if form.is_valid():
            participant = form.save(commit=False)

            participant.save()
            
            return redirect("settings")
    form = EditForm(instance=participant_obj)

   
    return render(
        request,
        "user/profile.html",
        {
            "form": form,
            "participant_obj": participant_obj,
            
            
            "previllage": previllage,
        },
    )


def registeredevents(request):
    previllage = Privillage.objects.filter(userid=request.user).first()

    userevent = User_Event.objects.filter(user_id=request.user).all()
    print(userevent)

    return render(
        request, "user/registeredevents.html", {"event": userevent, "previllage": previllage}
    )


def submitedpaper(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(userid=request.user).all()

    return render(
        request, "user/submitedpaper.html", {"paper": paper, "previllage": previllage}
    )


def submitedposter(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = PosterSubmition.objects.filter(userid=request.user).all()

    return render(
        request, "user/submitedposter.html", {"poster": poster, "previllage": previllage}
    )

def submitedcontext(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    context = ContextSubmition.objects.filter(userid=request.user).all()

    return render(
        request, "user/submitedcontext.html", {"context": context, "previllage": previllage}
    )


def viewsubmitedpaper(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(id=id).first()

    form = EditPaperSubmitionForm(instance=paper)

    if request.method == "POST":
        form = EditPaperSubmitionForm(
            request.POST,
            request.FILES,
            instance=paper,
        )
        if form.is_valid():
            p=form.save(commit=False)
            p.submit_count=1
            p.save()
            return redirect("submitedpaper")

    return render(
        request,
        "user/viewsubmitedpaper.html",
        {"paper": paper, "form": form, "previllage": previllage},
    )


def viewsubmitedposter(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = PosterSubmition.objects.filter(id=id).first()

    form = EditPosterSubmitionForm(instance=poster)

    if request.method == "POST":
        form = EditPosterSubmitionForm(request.POST, request.FILES, instance=poster)
        if form.is_valid():
            form.save()
            return redirect("submitedposter")

    return render(
        request,
        "user/viewsubmitedposter.html",
        {"poster": poster, "form": form, "previllage": previllage},
    )

def viewsubmitedcontext(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    context = ContextSubmition.objects.filter(id=id).first()

    form = EditContextSubmitionForm(instance=context)

    if request.method == "POST":
        form = EditContextSubmitionForm(request.POST, request.FILES, instance=context)
        if form.is_valid():
            form.save()
            return redirect("submitedcontext")

    return render(
        request,
        "user/viewsubmitedcontext.html",
        {"context": context, "form": form, "previllage": previllage},
    )
