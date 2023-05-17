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
#this code defines a view function for rendering the dashboard page.
#  It retrieves all events from the Event model and prints them (possibly for debugging purposes). 
# It then gets the current user and their privilege by filtering the Privillage model. Next,
#  it retrieves the participant object for the current user. Finally, 
# it renders the dashboard.html template with the events, participant object, privilege, and the current date.



def dashboard(request):
    # Retrieve all events
    events = Event.objects.all()
    print(events)

    # Get the current user and their privilege
    user = request.user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve the participant object for the current user
    participant_obj = Participant.objects.filter(user=user).first()

    return render(
        request,
        "user/dashboard.html",
        {
            "event": events,
            "participant": participant_obj,
            "previllage": previllage,
            "today": date.today(),
        },
    )

# this code defines a view function for handling event registration. 
# If the user is authenticated, it retrieves the privilege object and the User_Event object for the current user and event.
#  It also retrieves the event object and creates the paper and poster submission forms.
#  If a POST request is received, it processes the paper and poster submission forms, updates privilege and user_event objects, saves the submission objects, and sends email notifications to the user.
#  Finally, it renders the eventregistration.html template with the necessary data. If the user is not authenticated, 
# it redirects them to the login page.



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

#this code registers the current user as a participant for a specific event.
#  It retrieves the event object and the User_Event object for the current user and event.
#  If the User_Event object doesn't exist, a new object is created and saved with the corresponding event and user IDs.
# If the User_Event object already exists, it is updated to set the paper and poster fields to False.
#  An email notification is sent to the user to confirm their successful registration.
#  Finally, the user is redirected to the event registration page for the specified event.
def register_as_participant(request, event_id):
    # Retrieve the event object
    events = Event.objects.get(pk=event_id)

    # Retrieve the User_Event object for the current user and event
    user_events = User_Event.objects.filter(event_id=event_id, user_id=request.user).first()
    print(user_events)

    if user_events is None:
        # Create a new User_Event object if it doesn't exist
        user_event = User_Event()
        user_event.event_id = events
        user_event.user_id = request.user
        user_event.paper = False
        user_event.poster = False
        user_event.save()
    else:
        # Update the existing User_Event object
        user_events.paper = False
        user_events.poster = False
        user_events.save()

    # Send email notification to the user
    to_email = user_event.user_id.email
    subject = "You are successfully registered as a participant"
    message = f"You are successfully registered as a participant for {events.title}"
    sent_mail_from(to_email, subject, message)

    return redirect("eventregistration", event_id)


# this code handles the user's context registration for a specific event.
#  It first checks if the request method is POST. Then, it retrieves the event object.
#  The code creates an instance of the ContextSubmitionForm using the request data. 
# If the form is valid, it updates the user's privileges and event participation, saves the context submission,
#  and sends an email notification to the user. 
# Finally, the user is redirected to the event registration page for the specified event.


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
        

   # this function is to edit the users profile 

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
            "participant": participant_obj,
            
            "previllage": previllage,
        },
    )

# this fuction is to view the registered events 
def registeredevents(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    participant_obj = Participant.objects.filter(user=request.user).first()

    userevent = User_Event.objects.filter(user_id=request.user).all()
    print(userevent)

    return render(
        request, "user/registeredevents.html", {"event": userevent, "previllage": previllage,"participant": participant_obj}
    )

#this function is to render the status of submitted paper
def submitedpaper(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(userid=request.user).all()
    participant_obj = Participant.objects.filter(user=request.user).first()


    return render(
        request, "user/submitedpaper.html", {"paper": paper, "previllage": previllage,"participant": participant_obj}
    )

#this function is to render the status of submitted poster
def submitedposter(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = PosterSubmition.objects.filter(userid=request.user).all()
    participant_obj = Participant.objects.filter(user=request.user).first()


    return render(
        request, "user/submitedposter.html", {"poster": poster, "previllage": previllage,"participant": participant_obj,}
    )
#this function is to render the status of submitted context
def submitedcontext(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    context = ContextSubmition.objects.filter(userid=request.user).all()
    participant_obj = Participant.objects.filter(user=request.user).first()


    return render(
        request, "user/submitedcontext.html", {"context": context, "previllage": previllage,"participant": participant_obj}
    )

#this function is to view the details of submitted paper
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

def camera_ready_paper_submition(request,paper_id):

    camera_ready_paper=PaperSubmition.objects.filter(id=paper_id).first()

    if request.method == "POST":
        form=CameraReadyPaperSubmitionForm(request.POST,request.FILES,instance=camera_ready_paper)
        if form.is_valid():
            camera_paper=form.save(commit=False)
            camera_paper.camera_ready_submition_status='pending'
            camera_paper.save()
            to_email=camera_ready_paper.userid.email
            subject = "your are successfully submitted camera ready paper"
            message = f"your are successfully submitted camera ready paper for {camera_ready_paper.event.title}"
            sent_mail_from(to_email,subject,message)
            return redirect('viewsubmitedpaper',paper_id)

def camera_ready_poster_submition(request,id):
    camera_ready_poster=PosterSubmition.objects.filter(id=id).first()

    if request.method == "POST":
        form=CameraReadyPosterSubmitionForm(request.POST,request.FILES,instance=camera_ready_poster)
        if form.is_valid():
            camera_poster=form.save(commit=False)
            camera_poster.camera_ready_submition_status='pending'
            camera_poster.save()
            to_email=camera_ready_poster.userid.email
            subject = "your are successfully submitted camera ready Poster"
            message = f"your are successfully submitted camera ready poster for {camera_ready_poster.event.title}"
            sent_mail_from(to_email,subject,message)
            return redirect('viewsubmitedposter',id)
def camera_ready_context_submition(request,id):
    camera_ready_context=ContextSubmition.objects.filter(id=id).first()

    if request.method == "POST":
        form=CameraReadyContextSubmitionForm(request.POST,request.FILES,instance=camera_ready_context)
        if form.is_valid():
            camera_context=form.save(commit=False)
            camera_context.camera_ready_submition_status='pending'
            camera_context.save()
            to_email=camera_ready_context.userid.email
            subject = "your are successfully submitted camera ready context"
            message = f"your are successfully submitted camera ready context for {camera_ready_context.event.title}"
            sent_mail_from(to_email,subject,message)
            return redirect('viewsubmitedcontext',id)
#this function is to view the details of submitted poster
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
#this function is to view the details of submitted context
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
