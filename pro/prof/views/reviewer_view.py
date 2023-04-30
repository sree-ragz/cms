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








def reviewertable(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    reviewerpaper = Reviewer_Paper.objects.filter(userid=request.user).all()
    reviewerposter = Reviewer_Poster.objects.filter(userid=request.user).all()
    reviewercontext=Reviewer_Context.objects.filter(userid=request.user).all()
    return render(
        request,
        "reviewer/reviewertable.html",
        {
            "reviewerpaper": reviewerpaper,
            "reviewerposter": reviewerposter,
            "reviewercontext":reviewercontext,
            "user": request.user,
            "previllage": previllage,
        },
    )


def reviewerposterpage(request, id):
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


            return redirect("reviewertable")

    return render(
        request,
        "reviewer/reviewerposterpage.html",
        {"obj": poster, "form": form, "previllage": previllage},
    )


def reviewercontextpage(request, id):
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
                message = f"your context is accepted fot {context.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=context.userid.email
                subject = "your context is declined"
                message = f"your context is declined fot {context.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("reviewertable")

    return render(
        request,
        "reviewer/reviewercontextpage.html",
        {"obj": context, "form": form, "previllage": previllage},
    )


def reviewerpaperpage(request, id):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(id=id).first()
    print(paper.id)

    form = EditPaperrSubmitionFormReviewer(instance=paper)

    if request.method == "POST":     
        form = EditPaperrSubmitionFormReviewer(
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
                message = f"your paper is accepted fot {paper.event.title} conference"
                sent_mail_from(to_email,subject,message)
            elif status == 'declined':
                to_email=paper.userid.email
                subject = "your paper is declined"
                message = f"your paper is declined fot {paper.event.title} conference"
                sent_mail_from(to_email,subject,message)

            return redirect("reviewertable")

    return render(
        request,
        "reviewer/reviewerpaperpage.html",
        {"obj": paper, "form": form, "previllage": previllage},
    )