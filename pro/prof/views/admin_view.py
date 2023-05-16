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

#Overall, this code appears to be a view function for handling requests related to event administration. 
# It retrieves privileges, events, participant types, and form data. 
# It saves the form data if the request method is POST and renders the appropriate template with the necessary context.
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

#function for handling requests to edit an event. It checks if the request method is POST,
#  retrieves the event with the given id, creates an instance of the AdminAddorEditEvent form with the POST data and the event instance
# , and saves the form data if it is valid. Finally, it redirects the user to the "admin_event_list" URL in both cases.
def admin_edit_event(request, id):
    if request.method == "POST":
        event = Event.objects.filter(id=id).first()

        form = AdminAddorEditEvent(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect("admin_event_list")

    return redirect("admin_event_list")

#function for admin to delete an event
def admin_delete_event(request, id):
    event = Event.objects.filter(id=id).first().delete()
    return redirect("admin_event_list")

# this function is to assign the respected reviewer for paper reviewing
#code defines a view function for handling requests related to reviewer papers in the admin section.

#  It retrieves the privilege of the current user, all paper submissions, reviewer papers, and privileges of reviewers.
#  It creates an instance of the AdminAddorEditReviewerPaper form. If the request method is POST and the form data is valid,
#  it saves the form data and redirects to the "admin_reviewer_paper" URL. Finally,
#  it renders the appropriate template with the necessary context.
def admin_reviewer_paper(request):
    
    previllage = Privillage.objects.filter(userid=request.user).first()  # Retrieve the privilege of the current user
    ps=PaperSubmition.objects.all()                                         # Retrieve all reviewer papers
    paper = Reviewer_Paper.objects.all()
    p = Privillage.objects.filter(is_reviewer=True)
    

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
# this function is to assign the respected reviewer for context reviewing
#defines a view function for handling requests related to reviewer contexts in the admin section. 
# It retrieves the privilege of the current user, all context submissions, reviewer contexts, and privileges of reviewers.
#  It creates an instance of the AdminAddorEditReviewerContext form. If the request method is POST and the form data is valid, it saves the form data and redirects to the "admin_reviewer_context" URL. 
# Finally, it renders the appropriate template with the necessary context.
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




#this admin_edit_reviewer_context function is to edit the reviewer assigned for reviewing context
def admin_edit_reviewer_context(request, id):
    if request.method == "POST":
        context = Reviewer_Context.objects.filter(id=id).first()
        form = AdminAddorEditReviewerContext(request.POST, request.FILES, instance=context)
        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_context")
    return redirect("admin_reviewer_context")
# this function is to delete the reviewer assigned for context 
def admin_delete_reviewer_context(request, id):
    Reviewer_Context.objects.filter(id=id).delete()
    return redirect("admin_reviewer_context")

#this admin_edit_reviewer_context function is to edit the reviewer assigned for reviewing paper
def admin_edit_reviewer_paper(request, id):
    if request.method == "POST":
        paper = Reviewer_Paper.objects.filter(id=id).first()
        form = AdminAddorEditReviewerPaper(request.POST, request.FILES, instance=paper)
        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_paper")
    return redirect("admin_reviewer_paper")

# this function is to delete the reviewer assigned for paper 
def admin_delete_reviewer_paper(request, id):
    Reviewer_Paper.objects.filter(id=id).delete()
    return redirect("admin_reviewer_paper")

#this code defines a view function for handling requests related to reviewer posters in the admin section.
#  It retrieves the privilege of the current user, all reviewer posters, privileges of reviewers,
#  and all poster submissions. It creates an instance of the AdminAddorEditReviewerPoster form.
#  If the request method is POST and the form data is valid, it saves the form data and redirects to the "admin_reviewer_poster" URL.
#  Finally, it renders the appropriate template with the necessary context.
def admin_reviewer_poster(request):
    # Retrieve the privilege of the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve all reviewer posters
    poster = Reviewer_Poster.objects.all()

    # Retrieve all privileges where is_reviewer=True
    p = Privillage.objects.filter(is_reviewer=True)

    # Retrieve all poster submissions
    ps = PosterSubmition.objects.all()

    # Create an instance of the AdminAddorEditReviewerPoster form
    form = AdminAddorEditReviewerPoster()

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of the AdminAddorEditReviewerPoster form with the POST data
        form = AdminAddorEditReviewerPoster(request.POST, request.FILES)

        # Check if the form data is valid
        if form.is_valid():
            # Save the form data
            form.save()
            # Redirect to the "admin_reviewer_poster" URL
            return redirect("admin_reviewer_poster")

    # Render the "admin/admin_reviewer_poster.html" template with the provided context
    return render(
        request,
        "admin/admin_reviewer_poster.html",
        {"poster": poster, "form": form, "previllage": previllage, "reviewer": p, "ps": ps},
    )

#view function for handling requests to edit a reviewer poster in the admin section.
#  It checks if the request method is POST, retrieves the reviewer poster with the given id,
#  creates an instance of the AdminAddorEditReviewerPoster form with the POST data and the poster instance,
#  and saves the form data if it is valid. Finally, it redirects the user to the "admin_reviewer_poster" URL in both cases.



def admin_edit_reviewer_poster(request, id):
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the reviewer poster with the given id
        poster = Reviewer_Poster.objects.filter(id=id).first()

        # Create an instance of the AdminAddorEditReviewerPoster form with the POST data and the retrieved poster instance
        form = AdminAddorEditReviewerPoster(request.POST, request.FILES, instance=poster)
        
        # Check if the form data is valid
        if form.is_valid():
            # Save the form data
            form.save()
            # Redirect to the "admin_reviewer_poster" URL
            return redirect("admin_reviewer_poster")

    # Redirect to the "admin_reviewer_poster" URL
    return redirect("admin_reviewer_poster")


#function for delete reviewer assigned for poster
def admin_delete_reviewer_poster(request, id):
    Reviewer_Poster.objects.filter(id=id).delete()
    return redirect("admin_reviewer_poster")

#this code defines a view function for handling requests to add a reviewer in the admin section. 
# It retrieves the privilege of the current user, all reviewer privileges, and creates an instance of the CreateUserForm.
#  If the request method is POST and the form data is valid, it saves the form data, retrieves the newly created user,
#  creates a new Privillage instance for the user with is_reviewer=True, and redirects to the "admin_add_reviewer" URL. 
# Finally, it renders the appropriate template with the necessary context.
def admin_add_reviewer(request):
    # Retrieve the privilege of the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve all privileges where is_reviewer=True
    pre = Privillage.objects.filter(is_reviewer=True).all()

    # Create an instance of the CreateUserForm
    form = CreateUserForm()

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of the CreateUserForm with the POST data
        form = CreateUserForm(request.POST)

        # Check if the form data is valid
        if form.is_valid():
            # Get the username from the form data
            username = form.cleaned_data.get("username")

            # Save the form data
            form.save()

            # Retrieve the newly created user
            user = User.objects.filter(username=username).first()

            # Create a new Privillage instance for the user and set is_reviewer=True
            privillage = Privillage()
            privillage.userid = user
            privillage.is_reviewer = True
            privillage.save()

            # Redirect to the "admin_add_reviewer" URL
            return redirect("admin_add_reviewer")

    # Render the "admin/reviewers.html" template with the provided context
    return render(
        request, "admin/reviewers.html", {"form": form, "previllage": previllage, "pre": pre}
    )

#function for delete reviewer
def admin_delete_reviewer(request, name):
    User.objects.filter(username=name).delete()
    return redirect("admin_add_reviewer")


#function for delete chair and cochair
def admin_delete_chair_cochair(request, name):
    User.objects.filter(username=name).delete()
    return redirect("admin_add_chair_and_cochair")




# this code defines a view function for handling requests to add a chair or co-chair in the admin section.
#  It retrieves the privilege of the current user, details of existing chairs and co-chairs, 
# and creates an instance of the CreateChairAndCochairForm. If the request method is POST and the form data is valid, 
# it saves the form data, retrieves the newly created user, creates a new Privillage instance for the user, 
# and sets the chair or co_chair attribute based on the selected value of 'chair'. Finally, 
# it redirects to the "admin_add_chair_and_cochair" URL and renders the appropriate template with the necessary context.
def admin_add_chair_and_cochair(request):

    # Retrieve the privilege of the current user
    previllage = Privillage.objects.filter(userid=request.user).first()

    # Retrieve all privileges with chair=True
    chairdetails = Privillage.objects.filter(chair=True).all()

    # Retrieve all privileges with co_chair=True
    cochairdetails = Privillage.objects.filter(co_chair=True).all()

    # Create an instance of the CreateChairAndCochairForm
    form = CreateChairAndCochairForm()

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of the CreateChairAndCochairForm with the POST data
        form = CreateChairAndCochairForm(request.POST)
        chair = request.POST.get("chair_or_cochair")

        # Check if the form data is valid
        if form.is_valid():
            # Get the username from the form data
            username = form.cleaned_data.get("username")

            # Save the form data
            form.save()

            # Retrieve the newly created user
            user = User.objects.filter(username=username).first()

            # Create a new Privillage instance for the user and set the appropriate chair/co-chair attribute based on the value of 'chair'
            privillage = Privillage()
            privillage.userid = user
            if chair == 'chair':
                privillage.chair = True
            elif chair == 'cochair':
                privillage.co_chair = True
            privillage.save()

            # Redirect to the "admin_add_chair_and_cochair" URL
            return redirect("admin_add_chair_and_cochair")

    # Render the "admin/admin_add_chair_and_cochair.html" template with the provided context
    return render(request, 'admin/admin_add_chair_and_cochair.html', {"previllage": previllage, "chairdetails": chairdetails, "cochairdetails": cochairdetails})


#this function is to render all the registered participants details 
def admin_registered_user(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    participants=Participant.objects.all()
    


    return render(request,"admin/registered_user.html",{"previllage":previllage,"participants":participants})

# this admin_activate_deactivate_user function is to acivate and deactivate participants
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

    form = EditPaperSubmitionFormAdmin(instance=paper)

    if request.method == "POST":    
        print("jjjjj") 
        form = EditPaperSubmitionFormAdmin(
            request.POST, request.FILES, instance=paper
        )
        if form.is_valid():
            
            p=form.save(commit=False)
            p.submit_count=0
            p.save()
            

            return redirect("admin_reviewer_paper")
        

    return redirect("admin_reviewer_paper")
    
#this code defines a view function for handling requests to edit a poster submission in the admin section.
#  It retrieves the poster submission with the given id and creates an instance of the EditPosterSubmitionFormReviewer 
# form with the poster instance. If the request method is POST and the form data is valid, 
# it updates the submit_count attribute of the form to 0, saves the form data, and redirects to the "admin_reviewer_poster" 
# URL. Finally, it redirects to the "admin_reviewer_poster" URL in both cases.

def admin_edit_posterpage(request, id):
    # Retrieve the poster submission with the given id
    poster = PosterSubmition.objects.filter(id=id).first()

    # Print the 'posterremark' attribute of the poster
    print(poster.posterremark)

    # Create an instance of the EditPosterSubmitionFormReviewer with the poster instance
    form = EditPosterSubmitionFormAdmin(instance=poster)

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of the EditPosterSubmitionFormReviewer with the POST data and the poster instance
        form =EditPosterSubmitionFormAdmin(request.POST, request.FILES, instance=poster)

        # Check if the form data is valid
        if form.is_valid():
            # Update the 'submit_count' attribute to 0
            form.submit_count = 0
            # Save the form data
            form.save()
            # Redirect to the "admin_reviewer_poster" URL
            return redirect("admin_reviewer_poster")

    # Redirect to the "admin_reviewer_poster" URL
    return redirect("admin_reviewer_poster")

#this code defines a view function for handling requests to edit a context submission in the admin section.
#  It retrieves the context submission with the given id and creates an instance of the EditContextSubmitionFormReviewer
#  form with the context instance. If the request method is POST and the form data is valid, it updates the submit_count
#  attribute of the form to 0, saves the form data, and redirects to the "admin_reviewer_poster" URL. Finally, 
# it redirects to the "admin_reviewer_poster" URL in both cases.
def admin_edit_contextpage(request, id):
    # Retrieve the context submission with the given id
    context = ContextSubmition.objects.filter(id=id).first()

    # Create an instance of the EditContextSubmitionFormReviewer with the context instance
    form = EditContextSubmitionFormAdmin(instance=context)

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of the EditContextSubmitionFormReviewer with the POST data and the context instance
        form = EditContextSubmitionFormAdmin(request.POST, request.FILES, instance=context)

        # Check if the form data is valid
        if form.is_valid():
            # Update the 'submit_count' attribute to 0
            form.submit_count = 0
            # Save the form data
            form.save()
            # Redirect to the "admin_reviewer_poster" URL
            return redirect("admin_reviewer_poster")

    # Redirect to the "admin_reviewer_poster" URL
    return redirect("admin_reviewer_poster")

