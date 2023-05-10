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

from prof.views.sent_mail import sent_mail_from
from django.contrib.auth import get_user_model
from datetime import date








# this function takes a request object as input, and returns an HTTP response with a rendered template.
#  It retrieves the total count of Event, Participant, PaperSubmition, and PosterSubmition objects, 
# and the Privillage object associated with the current user (if any), and passes them as context variables to the admin_page.html template.
#  The template can use these variables to display various statistics and options for the administrator.

def admin_page(request):
    event = Event.objects.all().count()
    participant = Participant.objects.all().count()
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.all().count()
    poster = PosterSubmition.objects.all().count()

    return render(
        request,
        "admin/admin_page.html",
        {
            "previllage": previllage, # Pass the previllage object to the template as a context variable
            "event": event,                                               
            "participant": participant,
            "paper": paper,
            "poster": poster,
        },
    )


def admin_event_list(request, id=0):
    previllage = Privillage.objects.filter(userid=request.user).first()
    chair=Privillage.objects.filter(chair=True).all()
    cochair=Privillage.objects.filter(co_chair=True).all()

    events = Event.objects.all()

    addform = AdminAddorEditEvent()
    pt = ParticipantType.objects.all()
    print(pt)

    if request.method == "POST":
        addform = AdminAddorEditEvent(request.POST, request.FILES)
        if addform.is_valid():
            addform.save()
            return redirect("admin_event_list")

    return render(
        request,
        "admin/admin_event_list.html",
        {"previllage": previllage, "event": list(events), "form": addform, "pt": pt,
         "chair":chair,"cochair":cochair},
    )


def admin_edit_event(request, id):
    if request.method == "POST":
        event = Event.objects.filter(id=id).first()

        form = AdminAddorEditEvent(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("admin_event_list")

    return redirect("admin_event_list")


def admin_delete_event(request, id):
    event = Event.objects.filter(id=id).first().delete()
    return redirect("admin_event_list")


def admin_reviewer_paper(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    ps=PaperSubmition.objects.all()
    paper = Reviewer_Paper.objects.all()
    p = Privillage.objects.filter(is_reviewer=True)
    # print(p.first().userid.username)

    form = AdminAddorEditReviewerPaper()
    if request.method == "POST":
        form = AdminAddorEditReviewerPaper(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_paper")

    return render(
        request,
        "admin/admin_reviewer_paper.html",
        {"paper": paper, "form": form, "previllage": previllage, "reviewer": p,'ps':ps},
    )

def admin_reviewer_context(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    cs=ContextSubmition.objects.all()
    context = Reviewer_Context.objects.all()
    p = Privillage.objects.filter(is_reviewer=True)

    form=AdminAddorEditReviewerContext()
    if request.method == "POST":
        form = AdminAddorEditReviewerContext(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_context")




    return render(
        request,
        "admin/admin_reviewer_context.html",
        {"context": context,"previllage": previllage, "reviewer": p,'cs':cs},
    )
def admin_edit_reviewer_context(request, id):
    if request.method == "POST":
        context = Reviewer_Context.objects.filter(id=id).first()
        form = AdminAddorEditReviewerContext(request.POST, request.FILES, instance=context)
        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_context")
    return redirect("admin_reviewer_context")

def admin_delete_reviewer_context(request, id):
    Reviewer_Context.objects.filter(id=id).delete()
    return redirect("admin_reviewer_context")


def admin_edit_reviewer_paper(request, id):
    if request.method == "POST":
        paper = Reviewer_Paper.objects.filter(id=id).first()
        form = AdminAddorEditReviewerPaper(request.POST, request.FILES, instance=paper)
        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_paper")
    return redirect("admin_reviewer_paper")


def admin_delete_reviewer_paper(request, id):
    Reviewer_Paper.objects.filter(id=id).delete()
    return redirect("admin_reviewer_paper")


def admin_reviewer_poster(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = Reviewer_Poster.objects.all()
    p = Privillage.objects.filter(is_reviewer=True)
    ps=PosterSubmition.objects.all()

    form = AdminAddorEditReviewerPoster()
    if request.method == "POST":
        form = AdminAddorEditReviewerPoster(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_poster")

    return render(
        request,
        "admin/admin_reviewer_poster.html",
        {"poster": poster, "form": form, "previllage": previllage,'reviewer':p,'ps':ps},
    )


def admin_edit_reviewer_poster(request, id):
    if request.method == "POST":
        poster = Reviewer_Poster.objects.filter(id=id).first()
        form = AdminAddorEditReviewerPoster(
            request.POST, request.FILES, instance=poster
        )
        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_poster")
    return redirect("admin_reviewer_poster")


def admin_delete_reviewer_poster(request, id):
    Reviewer_Poster.objects.filter(id=id).delete()
    return redirect("admin_reviewer_poster")


def admin_add_reviewer(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    pre = Privillage.objects.filter(is_reviewer=True).all()
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")

            form.save()
            user = User.objects.filter(username=username).first()
            privillage = Privillage()
            privillage.userid = user
            privillage.is_reviewer = True
            privillage.save()
            return redirect("admin_add_reviewer")
    return render(
        request, "admin/reviewers.html", {"form": form, "previllage": previllage, "pre": pre}
    )


def admin_delete_reviewer(request, name):
    User.objects.filter(username=name).delete()
    return redirect("admin_add_reviewer")

def admin_delete_chair_cochair(request, name):
    User.objects.filter(username=name).delete()
    return redirect("admin_add_chair_and_cochair")

def admin_add_chair_and_cochair(request):


    previllage = Privillage.objects.filter(userid=request.user).first()
    chairdetails= Privillage.objects.filter(chair=True).all()
    cochairdetails= Privillage.objects.filter(co_chair=True).all()


    form = CreateChairAndCochairForm()
    if request.method == "POST":
        form = CreateChairAndCochairForm(request.POST)
        chair=request.POST.get("chair_or_cochair")

        if form.is_valid():
            username = form.cleaned_data.get("username")
            
            print(chair)

            form.save()
            user = User.objects.filter(username=username).first()
            privillage = Privillage()
            privillage.userid = user
            if chair == 'chair':
             privillage.chair = True
            elif chair == 'cochair' :
             privillage.co_chair = True
            privillage.save()
            return redirect("admin_add_chair_and_cochair")

    return render(request,'admin/admin_add_chair_and_cochair.html', {"previllage": previllage, "chairdetails": chairdetails,"cochairdetails":cochairdetails})





def admin_registered_user(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    participants=Participant.objects.all()
    


    return render(request,"admin/registered_user.html",{"previllage":previllage,"participants":participants})


def admin_activate_deactivate_user(request,id):
    participant=Participant.objects.filter(id=id).first()

    if request.method == "POST":
        print("helloo")

        form=AdminUser(request.POST,instance=participant)
        if form.is_valid():
            form.save()

            return redirect("admin_registered_user")
        


#this function takes a request object and an ID parameter as input,
#  and returns an HTTP redirect response. It retrieves a PaperSubmition object with the given ID, 
# creates an instance of the EditPaperrSubmitionFormAdmin form with the retrieved object, processes the form data
#  if the request method is POST, saves the updated object to the database, 
# and redirects the user to the admin_reviewer_paper view. 
# The function also includes some print statements for debugging purposes.

def admin_edit_paperpage(request,id):
    
    paper = PaperSubmition.objects.filter(id=id).first()
    print("he",paper.id)

    form = EditPaperrSubmitionFormAdmin(instance=paper)

    if request.method == "POST":    
        print("jjjjj") 
        form = EditPaperrSubmitionFormAdmin(
            request.POST, request.FILES, instance=paper
        )
        if form.is_valid():
            
            p=form.save(commit=False)
            p.submit_count=0
            p.save()
            

            return redirect("admin_reviewer_paper")
        

    return redirect("admin_reviewer_paper")
    


def admin_edit_posterpage(request, id):
    
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
            

            return redirect("admin_reviewer_poster")

    return redirect("admin_reviewer_poster")



def admin_edit_contextpage(request, id):
  
    context = ContextSubmition.objects.filter(id=id).first()
    

    form =  EditContextSubmitionFormReviewer(instance=context)

    if request.method == "POST":
        form = EditContextSubmitionFormReviewer(
            request.POST, request.FILES, instance=context
        )

        if form.is_valid():
            form.submit_count = 0
            form.save()
           

            return redirect("admin_reviewer_poster")

    return redirect("admin_reviewer_poster")

