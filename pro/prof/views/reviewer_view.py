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





#this code defines a view function for rendering the reviewer table page.
#  It retrieves the Privillage object for the current user and fetches the reviewer papers, 
# posters, and contexts associated with the user. The function then renders the "reviewertable.html" template,
#  passing in the retrieved data along with the current user and previllage information.

@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewertable(request):
    # Retrieve the Privillage object for the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve the reviewer papers, posters, and contexts for the current user
    reviewerpaper = Reviewer_Paper.objects.filter(userid=request.user).all()
    reviewerposter = Reviewer_Poster.objects.filter(userid=request.user).all()
    reviewercontext = Reviewer_Context.objects.filter(userid=request.user).all()

    # Render the reviewertable.html template with the necessary data
    return render(
        request,
        "reviewer/reviewertable.html",
        {
            "reviewerpaper": reviewerpaper,
            "reviewerposter": reviewerposter,
            "reviewercontext": reviewercontext,
            "user": request.user,
            "previllage": previllage,
        },
    )

# this code defines a view function for rendering the reviewer's poster page.
#  It retrieves the Privillage object for the current user and fetches the poster submission object with the given ID. 
# The function then creates an instance of the EditPosterSubmitionFormReviewer form using the retrieved poster object.
#  If the request method is POST, the function processes the form submission, saves the form data, 
# and sends an email notification based on the status of the poster.
# Finally, the function renders the "reviewerposterpage.html" template, passing in the poster object, the form, and the previllage information.
@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewerposterpage(request, id):
    # Retrieve the Privillage object for the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve the poster submission object with the given id
    poster = PosterSubmition.objects.filter(id=id).first()
    print(poster.posterremark)

    # Create an instance of the EditPosterSubmitionFormReviewer form with the poster object
    form = EditPosterSubmitionFormReviewer(instance=poster)

    if request.method == "POST":
        # If the request method is POST, process the form submission
        form = EditPosterSubmitionFormReviewer(
            request.POST, request.FILES, instance=poster
        )

        if form.is_valid():
            # If the form is valid, save the form data
            form.submit_count = 0
            form.save()
            status = form.cleaned_data['status']
            
            # Send an email notification based on the status of the poster
            if status == 'accepted':
                to_email = poster.userid.email
                subject = "Your poster is accepted"
                message = f"Your poster is accepted for the {poster.event.title} conference"
                sent_mail_from(to_email, subject, message)
            elif status == 'declined':
                to_email = poster.userid.email
                subject = "Your poster is declined"
                message = f"Your poster is declined for the {poster.event.title} conference"
                sent_mail_from(to_email, subject, message)

            return redirect("reviewertable")

    # Render the reviewerposterpage.html template with the necessary data
    return render(
        request,
        "reviewer/reviewerposterpage.html",
        {"obj": poster, "form": form, "previllage": previllage},
    )

#this code defines a view function for rendering the reviewer's context page. 
# It retrieves the Privillage object for the current user and fetches the context submission object with the given ID. 
# The function then creates an instance of the EditContextSubmitionFormReviewer form using the retrieved context object. 
# If the request method is POST, the function processes the form submission, saves the form data,
#  and sends an email notification based on the status of the context submission.
#  Finally, the function renders the "reviewercontextpage.html" template, passing in the context object, the form, 
# and the previllage information.
@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewercontextpage(request, id):
    # Retrieve the Privillage object for the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve the context submission object with the given id
    context = ContextSubmition.objects.filter(id=id).first()

    # Create an instance of the EditContextSubmitionFormReviewer form with the context object
    form =  EditContextSubmitionFormReviewer(instance=context)

    if request.method == "POST":
        # If the request method is POST, process the form submission
        form = EditContextSubmitionFormReviewer(
            request.POST, request.FILES, instance=context
        )

        if form.is_valid():
            # If the form is valid, save the form data
            form.submit_count = 0
            form.save()
            status = form.cleaned_data['status']

            # Send an email notification based on the status of the context submission
            if status == 'accepted':
                to_email = context.userid.email
                subject = "Your context is accepted"
                message = f"Your context is accepted for the {context.event.title} conference"
                sent_mail_from(to_email, subject, message)
            elif status == 'declined':
                to_email = context.userid.email
                subject = "Your context is declined"
                message = f"Your context is declined for the {context.event.title} conference"
                sent_mail_from(to_email, subject, message)

            return redirect("reviewertable")

    # Render the reviewercontextpage.html template with the necessary data
    return render(
        request,
        "reviewer/reviewercontextpage.html",
        {"obj": context, "form": form, "previllage": previllage},
    )

#this code defines a view function for rendering the reviewer's paper page. 
# It retrieves the Privillage object for the current user and fetches the paper submission object with the given ID.
#  The function then creates an instance of the EditPaperrSubmitionFormReviewer form using the retrieved paper object.
#  If the request method is POST, the function processes the form submission, saves the form data,
#  and sends an email notification based on the status of the paper submission. 
# Finally, the function renders the "reviewerpaperpage.html" template, passing in the paper object, the form, and the previllage information.
@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewerpaperpage(request, id):
    # Retrieve the Privillage object for the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve the paper submission object with the given id
    paper = PaperSubmition.objects.filter(id=id).first()
    print(paper.id)

    # Create an instance of the EditPaperrSubmitionFormReviewer form with the paper object
    form = EditPaperSubmitionFormReviewer(instance=paper)

    if request.method == "POST":
        # If the request method is POST, process the form submission
        form = EditPaperSubmitionFormReviewer(
            request.POST, request.FILES, instance=paper
        )
        if form.is_valid():
            # If the form is valid, save the form data
            p = form.save(commit=False)
            p.submit_count = 0
            p.save()
            status = form.cleaned_data["status"]

            # Send an email notification based on the status of the paper submission
            if status == 'accepted':
                to_email = paper.userid.email
                subject = "Your paper is accepted"
                message = f"Your paper is accepted for the {paper.event.title} conference"
                sent_mail_from(to_email, subject, message)
            elif status == 'declined':
                to_email = paper.userid.email
                subject = "Your paper is declined"
                message = f"Your paper is declined for the {paper.event.title} conference"
                sent_mail_from(to_email, subject, message)

            return redirect("reviewertable")

    # Render the reviewerpaperpage.html template with the necessary data
    return render(
        request,
        "reviewer/reviewerpaperpage.html",
        {"obj": paper, "form": form, "previllage": previllage},
    )

#this code defines a view function for handling the reviewer's camera-ready paper submission. 
# It retrieves the camera ready paper submission object with the given ID. 
# If the request method is POST, the function processes the form submission by instantiating and validating the 
# EditCameraReadyPaperSubmitionFormReviewer form. If the form is valid, 
# it saves the form data and sends an email notification to the author based on the status of the camera ready paper submission. Finally, the function redirects the user to the reviewertable page.
@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewer_camera_ready_paper(request, id):
    # Retrieve the camera ready paper submission object with the given id
    camera_ready_paper = PaperSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        # If the request method is POST, process the form submission
        form = EditCameraReadyPaperSubmitionFormReviewer(request.POST, request.FILES, instance=camera_ready_paper)

        if form.is_valid():
            # If the form is valid, save the form data
            form.save()
            status = form.cleaned_data["camera_ready_submition_status"]

            # Send an email notification based on the status of the camera ready paper submission
            if status == 'accepted':
                to_email = camera_ready_paper.userid.email
                subject = "Your camera-ready paper is accepted"
                message = f"Your camera-ready paper is accepted for the {camera_ready_paper.event.title} conference"
                sent_mail_from(to_email, subject, message)
            elif status == 'declined':
                to_email = camera_ready_paper.userid.email
                subject = "Your camera-ready paper is declined"
                message = f"Your camera-ready paper is declined for the {camera_ready_paper.event.title} conference"
                sent_mail_from(to_email, subject, message)

            return redirect('reviewertable')
@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewer_camera_ready_poster(request, id):
    # Retrieve the camera ready poster submission object with the given id
    camera_ready_poster = PosterSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        # If the request method is POST, process the form submission
        form = EditCameraReadyPosterSubmitionFormReviewer(request.POST, request.FILES, instance=camera_ready_poster)

        if form.is_valid():
            # If the form is valid, save the form data
            form.save()
            status = form.cleaned_data["camera_ready_submition_status"]

            # Send an email notification based on the status of the camera ready poster submission
            if status == 'accepted':
                to_email = camera_ready_poster.userid.email
                subject = "Your camera-ready poster is accepted"
                message = f"Your camera-ready poster is accepted for the {camera_ready_poster.event.title} conference"
                sent_mail_from(to_email, subject, message)
            elif status == 'declined':
                to_email = camera_ready_poster.userid.email
                subject = "Your camera-ready poster is declined"
                message = f"Your camera-ready poster is declined for the {camera_ready_poster.event.title} conference"
                sent_mail_from(to_email, subject, message)

            return redirect('reviewertable')

@login_required(login_url='login')
@allowed_users(allowed_roles=['reviewer'])
def reviewer_camera_ready_context(request, id):
    # Retrieve the camera ready context submission object with the given id
    camera_ready_context = ContextSubmition.objects.filter(id=id).first()

    if request.method == 'POST':
        # If the request method is POST, process the form submission
        form = EditCameraReadyContextSubmitionFormReviewer(request.POST, request.FILES, instance=camera_ready_context)

        if form.is_valid():
            # If the form is valid, save the form data
            form.save()
            status = form.cleaned_data["camera_ready_submition_status"]

            # Send an email notification based on the status of the camera ready context submission
            if status == 'accepted':
                to_email = camera_ready_context.userid.email
                subject = "Your camera-ready context is accepted"
                message = f"Your camera-ready context is accepted for the {camera_ready_context.event.title} conference"
                sent_mail_from(to_email, subject, message)
            elif status == 'declined':
                to_email = camera_ready_context.userid.email
                subject = "Your camera-ready context is declined"
                message = f"Your camera-ready context is declined for the {camera_ready_context.event.title} conference"
                sent_mail_from(to_email, subject, message)

            return redirect('reviewertable')
