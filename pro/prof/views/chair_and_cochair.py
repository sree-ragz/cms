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


@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_view(request):
    chair=Event.objects.filter(chair_id=request.user).all()
    previllage=Privillage.objects.filter(userid=request.user).first()
    print(chair)
    

    return render(request,'chair/chair_view.html',{"chair":chair,"previllage":previllage,"s":False}) 


@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_details(request,id):
    previllage=Privillage.objects.filter(userid=request.user).first()
    event=Event.objects.filter(id=id).first()
    addform = AdminAddorEditEvent()
    chair=Privillage.objects.filter(chair=True).all()
    cochair=Privillage.objects.filter(co_chair=True).all()
    total_registered=User_Event.objects.filter(event_id=id).all()
    total_paper=PaperSubmition.objects.filter(event=id).all()
    total_poster=PosterSubmition.objects.filter(event=id).all()
    total_context=ContextSubmition.objects.filter(event=id).all()
    print(total_context)


    return render(request,'chair/chair_details.html',
                  {"event":event,"form":addform,"chair":chair,"cochair":cochair,
                   "total_registered":total_registered,"total_paper":total_paper,
                   "total_poster":total_poster,"total_context": total_context,
                   "previllage":previllage
                   
                                                      })

@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_edit_event(request, id):
    if request.method == "POST":
        event = Event.objects.filter(id=id).first()

        form = AdminAddorEditEvent(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("chair_details",id)

    return redirect("chair_details",id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def registered_users(request):
    event=Event.objects.filter(chair_id=request.user).all()
    print(event)
    tr=[]
    for i in event:

        total_registered=User_Event.objects.filter(event_id=i.pk).all()
        tr+=total_registered

    previllage=Privillage.objects.filter(userid=request.user).first()

    print(tr)
    return render(request,"chair/registered_users.html",{"total_registered":tr,"previllage":previllage,"event":event})

@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_paper(request):
    event=Event.objects.filter(chair_id=request.user).all()
    p=[]
    for i in event:
        paper=PaperSubmition.objects.filter(event=i.pk).all()
        p+=paper
        
    previllage=Privillage.objects.filter(userid=request.user).first()

    
    return render(request,'chair/paper.html',{"paper":p,"event":event,"previllage":previllage})


@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_paper_details(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(id=id).first()
    event=Event.objects.filter(id=id).first()
    form = EditPaperSubmitionFormReviewer(instance=paper)
    print(event)
    if request.method == "POST":     
        form = EditPaperSubmitionFormReviewer(
            request.POST, request.FILES, instance=paper
        )
        if form.is_valid():
            p=form.save(commit=False)
            p.submit_count=0
            p.save()
            status=form.cleaned_data["status"]
            if status == 'accepted':
                to_email=paper.userid.email
                subject = "your paper is accepted"
                message = f"your paper is accepted for {paper.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=paper.userid.email
                subject = "your paper is declined"
                message = f"your paper is declined for {paper.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("chair_paper")

    return render(
        request,
        "chair/paper_details.html",
        {"obj": paper,"form":form,"previllage":previllage,"event":event}
    )

@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_camera_ready_paper(request,id):
    
    camera_ready_paper=PaperSubmition.objects.filter(id=id).first()
    if request.method == 'POST':
        form=EditCameraReadyPaperSubmitionFormReviewer(request.POST,request.FILES,instance=camera_ready_paper)

        if form.is_valid():
            form.save()
            status=form.cleaned_data["camera_ready_submition_status"]
            if status == 'accepted':
                to_email=camera_ready_paper.userid.email
                subject = "your camera raedy paper is accepted"
                message = f"your camera raedy paper is accepted for {camera_ready_paper.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=camera_ready_paper.userid.email
                subject = "your camera raedy paper is declined"
                message = f"your camera raedy paper for {camera_ready_paper.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("chair_paper",camera_ready_paper.event.id)
        


@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_poster(request):
    event=Event.objects.filter(chair_id=request.user).all()
    p=[]
    for i in event:
     poster=PosterSubmition.objects.filter(event=i.pk).all()
     p+=poster
    previllage=Privillage.objects.filter(userid=request.user).first()


    return render(request,'chair/poster.html',{"poster":p,"event":event,"previllage":previllage})
@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_poster_details(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = PosterSubmition.objects.filter(id=id).first()
    event=Event.objects.filter(id=id).first()
    form = EditPosterSubmitionFormReviewer(instance=poster)

    if request.method == "POST":
        form = EditPosterSubmitionFormReviewer(
            request.POST, request.FILES, instance=poster
        )

        if form.is_valid():
            form.submit_count = 0
            form.save()
            status=form.cleaned_data['status']
            if status == 'accepted':
                to_email=poster.userid.email
                subject = "your poster is accepted"
                message = f"your poster is accepted fot {poster.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=poster.userid.email
                subject = "your poster is declined"
                message = f"your poster is declined fot {poster.event.title} conference"
                sent_mail_from(to_email,subject,message)


            return redirect("chair_poster")

    return render(
        request,
        "chair/poster_details.html",
        {"obj": poster, "form": form,"previllage":previllage,}
    )

@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_camera_ready_poster(request,id):
    camera_ready_poster=PosterSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        form=EditCameraReadyPosterSubmitionFormReviewer(request.POST,request.FILES,instance=camera_ready_poster)

        if form.is_valid():
            form.save()
            status=form.cleaned_data["camera_ready_submition_status"]
            if status == 'accepted':
                to_email=camera_ready_poster.userid.email
                subject = "your camera raedy poster is accepted"
                message = f"your camera raedy poster is accepted for {camera_ready_poster.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=camera_ready_poster.userid.email
                subject = "your camera raedy poster is declined"
                message = f"your camera raedy poster for {camera_ready_poster.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect('chair_poster',camera_ready_poster.event.id)
        

@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_context(request):
    event=Event.objects.filter(chair_id=request.user).all()
    p=[]
    for i in event:
     context=ContextSubmition.objects.filter(event=i.pk).all()
     p+=context
    previllage=Privillage.objects.filter(userid=request.user).first()


    return render(request,'chair/context.html',{"context":p,"previllage":previllage})


@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_context_details(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    context = ContextSubmition.objects.filter(id=id).first()
    

    form =  EditContextSubmitionFormReviewer(instance=context)

    if request.method == "POST":
        form = EditContextSubmitionFormReviewer(
            request.POST, request.FILES, instance=context
        )

        if form.is_valid():
            form.submit_count = 0
            form.save()
            status=form.cleaned_data['status']
            if status == 'accepted':
                to_email=context.userid.email
                subject = "your context is accepted"
                message = f"your context is accepted for {context.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=context.userid.email
                subject = "your context is declined"
                message = f"your context is declined for {context.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("chair_context")

    return render(
        request,
        "chair/context_details.html",
        {"obj": context, "form": form, "previllage": previllage},
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['chair'])
def chair_camera_ready_context(request,id):
    camera_ready_context=ContextSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        form=EditCameraReadyContextSubmitionFormReviewer(request.POST,request.FILES,instance=camera_ready_context)

        if form.is_valid():
            form.save()
            status=form.cleaned_data["camera_ready_submition_status"]
            if status == 'accepted':
                to_email=camera_ready_context.userid.email
                subject = "your camera raedy context is accepted"
                message = f"your camera raedy context is accepted for {camera_ready_context.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=camera_ready_context.userid.email
                subject = "your camera raedy context is declined"
                message = f"your camera raedy context for {camera_ready_context.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect('chair_context',camera_ready_context.event.id)
        
@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])
def co_chair_view(request):
    cochair=Event.objects.filter(co_chair_id=request.user).all()
    
    previllage=Privillage.objects.filter(userid=request.user).first()
    

    return render(request,'cochair/cochair_view.html',{"cochair":cochair,"previllage":previllage})


@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_details(request,id):
    event=Event.objects.filter(id=id).first()
    addform = AdminAddorEditEvent()

    total_registered=User_Event.objects.filter(event_id=id).all()
    total_paper=PaperSubmition.objects.filter(event=id).all()
    total_poster=PosterSubmition.objects.filter(event=id).all()
    total_context=ContextSubmition.objects.filter(event=id).all()
    print(total_context)



    return render(request,'cochair/cochair_details.html',
                  {"event":event,"form":addform,
                   "total_registered":total_registered,"total_paper":total_paper,
                   "total_poster":total_poster,"total_context": total_context
                   
                                                      })

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_edit_event(request, id):
    if request.method == "POST":
        event = Event.objects.filter(id=id).first()

        form = AdminAddorEditEvent(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("cochair_details",id)

    return redirect("cochair_details",id)

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def cochair_registered_users(request):
    event=Event.objects.filter(co_chair_id=request.user).all()
    print(event)
    tr=[]
    for i in event:

        total_registered=User_Event.objects.filter(event_id=i.pk).all()
        tr+=total_registered

    previllage=Privillage.objects.filter(userid=request.user).first()

    

    
    return render(request,"cochair/registered_users.html",{"total_registered":tr,"previllage":previllage})

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_paper(request):
    event=Event.objects.filter(co_chair_id=request.user).all()
    p=[]
    for i in event:
     paper=PaperSubmition.objects.filter(event=i.pk).all()
     p+=paper
    
    previllage=Privillage.objects.filter(userid=request.user).first()


    return render(request,'cochair/paper.html',{"paper":p,"previllage":previllage})


@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_paper_details(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(id=id).first()
    print(paper.event)

    form = EditPaperSubmitionFormReviewer(instance=paper)

    if request.method == "POST":     
        form = EditPaperSubmitionFormReviewer(
            request.POST, request.FILES, instance=paper
        )
        if form.is_valid():
            
            p=form.save(commit=False)
            p.submit_count=0
            p.save()
            status=form.cleaned_data["status"]
            if status == 'accepted':
                to_email=paper.userid.email
                subject = "your paper is accepted"
                message = f"your paper is accepted for {paper.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=paper.userid.email
                subject = "your paper is declined"
                message = f"your paper is declined for {paper.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("chair_paper",paper.event.id)

    return render(
        request,
        "cochair/paper_details.html",
        {"obj": paper, "form": form, "previllage": previllage},
    )

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_camera_ready_paper(request,id):
    
    camera_ready_paper=PaperSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        form=EditCameraReadyPaperSubmitionFormReviewer(request.POST,request.FILES,instance=camera_ready_paper)

        if form.is_valid():
            form.save()
            status=form.cleaned_data["camera_ready_submition_status"]
            if status == 'accepted':
                to_email=camera_ready_paper.userid.email
                subject = "your camera raedy paper is accepted"
                message = f"your camera raedy paper is accepted for {camera_ready_paper.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=camera_ready_paper.userid.email
                subject = "your camera raedy paper is declined"
                message = f"your camera raedy paper for {camera_ready_paper.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("cochair_paper",camera_ready_paper.event.id)
        

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_poster(request):
    event=Event.objects.filter(co_chair_id=request.user).all()
    p=[]
    for i in event:
     poster=PosterSubmition.objects.filter(event=i.pk).all()
     p+=poster
    previllage=Privillage.objects.filter(userid=request.user).first()


    return render(request,'cochair/poster.html',{"poster":p,"previllage":previllage})
@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_poster_details(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = PosterSubmition.objects.filter(id=id).first()
    print(poster.posterremark)

    form = EditPosterSubmitionFormReviewer(instance=poster)

    if request.method == "POST":
        form = EditPosterSubmitionFormReviewer(
            request.POST, request.FILES, instance=poster
        )

        if form.is_valid():
            form.submit_count = 0
            form.save()
            status=form.cleaned_data['status']
            if status == 'accepted':
                to_email=poster.userid.email
                subject = "your poster is accepted"
                message = f"your poster is accepted fot {poster.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=poster.userid.email
                subject = "your poster is declined"
                message = f"your poster is declined fot {poster.event.title} conference"
                sent_mail_from(to_email,subject,message)


            return redirect("cochair_poster",poster.event.id)

    return render(
        request,
        "cochair/poster_details.html",
        {"obj": poster, "form": form, "previllage": previllage},
    )

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_camera_ready_poster(request,id):
    camera_ready_poster=PosterSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        form=EditCameraReadyPosterSubmitionFormReviewer(request.POST,request.FILES,instance=camera_ready_poster)

        if form.is_valid():
            form.save()
            status=form.cleaned_data["camera_ready_submition_status"]
            if status == 'accepted':
                to_email=camera_ready_poster.userid.email
                subject = "your camera raedy poster is accepted"
                message = f"your camera raedy poster is accepted for {camera_ready_poster.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=camera_ready_poster.userid.email
                subject = "your camera raedy poster is declined"
                message = f"your camera raedy poster for {camera_ready_poster.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect('cochair_poster',camera_ready_poster.event.id)
        

@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_context(request):
    event=Event.objects.filter(co_chair_id=request.user).all()
    p=[]
    for i in event:
     context=ContextSubmition.objects.filter(event=i.pk).all()
     p+=context
    previllage=Privillage.objects.filter(userid=request.user).first()


    return render(request,'cochair/cochair_context.html',{"context":p,"previllage":previllage})


@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_context_details(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    context = ContextSubmition.objects.filter(id=id).first()
    

    form =  EditContextSubmitionFormReviewer(instance=context)

    if request.method == "POST":
        form = EditContextSubmitionFormReviewer(
            request.POST, request.FILES, instance=context
        )

        if form.is_valid():
            form.submit_count = 0
            form.save()
            status=form.cleaned_data['status']
            if status == 'accepted':
                to_email=context.userid.email
                subject = "your context is accepted"
                message = f"your context is accepted for {context.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=context.userid.email
                subject = "your context is declined"
                message = f"your context is declined for {context.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("cochair_context",context.event.id)

    return render(
        request,
        "cochair/cochair_context_details.html",
        {"obj": context, "form": form, "previllage": previllage},
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['cochair'])

def co_chair_camera_ready_context(request,id):
    camera_ready_context=ContextSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        form=EditCameraReadyContextSubmitionFormReviewer(request.POST,request.FILES,instance=camera_ready_context)

        if form.is_valid():
            form.save()
            status=form.cleaned_data["camera_ready_submition_status"]
            if status == 'accepted':
                to_email=camera_ready_context.userid.email
                subject = "your camera raedy context is accepted"
                message = f"your camera raedy context is accepted for {camera_ready_context.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=camera_ready_context.userid.email
                subject = "your camera raedy context is declined"
                message = f"your camera raedy context for {camera_ready_context.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect('cochair_context',camera_ready_context.event.id)

