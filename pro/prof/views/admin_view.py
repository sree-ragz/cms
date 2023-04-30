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
            "previllage": previllage,
            "event": event,
            "participant": participant,
            "paper": paper,
            "poster": poster,
        },
    )


def admin_event_list(request, id=0):
    previllage = Privillage.objects.filter(userid=request.user).first()

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
        {"previllage": previllage, "event": list(events), "form": addform, "pt": pt},
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

