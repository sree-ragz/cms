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
from django.contrib.auth.models import Group
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import get_user_model
from datetime import date


from prof.views.sent_mail import sent_mail_from

# this code defines a view function for handling the login page.
#  If the request method is POST, it retrieves the username and password from the POST data and attempts to authenticate the user. 
# It then checks the role of the user and redirects to the appropriate page based on their privileges and participant status.
#  If the authentication or role check fails, appropriate error messages are displayed and the user is redirected back to the login page. 
# If an exception occurs during the process, an error message is returned. Finally, if the request method is not POST,
#  the login page is rendered.


def loginpage(request):
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the username and password from the POST data
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            # Retrieve the user object with the given username
            user_obj = User.objects.filter(username=username).first()

            # Check if the user object exists
            if user_obj is None:
                # Display a success message and redirect to the login page if the user is not found
                messages.success(request, "user not found")
                return redirect("/login")

            # Authenticate the user with the provided username and password
            user = authenticate(request, username=username, password=password)

            # Check if the authentication is successful
            if user is None:
                # Display a success message and redirect to the login page if the password is incorrect
                messages.success(request, "wrong password")
                return redirect("/login")

            # Retrieve the participant object associated with the user
            participant_obj = Participant.objects.filter(user=user).first()
            print(participant_obj)

            # Check if the participant is deactivated
            if participant_obj is not None and participant_obj.Rstatus == "d":
                # Display a success message and redirect to the login page if the account is deactivated
                messages.success(request, "account deactivated")
                return redirect("/login")

            # Authenticate the user again (to ensure login)
            user = authenticate(request, username=username, password=password)
            print(user)

            # Check the role of the user and redirect to the appropriate page
            if user is not None:
                login(request, user)
                previllage = Privillage.objects.filter(userid=user).first()
                print(previllage)

                if participant_obj is None and previllage is None:
                    # Redirect to the registration page if the user is not registered
                    return redirect("/register2")
                elif previllage.is_reviewer:
                    # Redirect to the reviewer table page if the user is a reviewer
                    return redirect("reviewertable")
                elif previllage.is_admin:
                    # Redirect to the admin page if the user is an admin
                    return redirect("admin_page")
                elif previllage.chair:
                    # Redirect to the chair view page if the user is a chair
                    return redirect("chair_view")
                elif previllage.co_chair:
                    # Redirect to the co-chair view page if the user is a co-chair
                    return redirect("cochair_view")
                elif previllage.participant:
                    # Redirect to the participant dashboard if the user is a participant
                    return redirect("dashboard")
        except Exception as e:
            # Return an error message if something goes wrong
            return HttpResponse("something went wrong")

    # Render the login page
    return render(request, "base/login.html")


#this code defines a view function for handling the user registration process.
#  It creates an instance of the CreateUserForm and checks if the request method is POST.
#  If it is, the form data is validated and processed. If the form data is valid,
#  it checks if the username and email are already taken. If not, 
# it saves the form data to create a new user with the is_active flag set to False. 
# It generates a verification email containing a unique link for the user to confirm their account. 
# The email is sent using the sent_mail_from function. 
# Success messages are displayed and the user is redirected to the register page.
#  If there are any exceptions or if the form data is invalid, appropriate error messages are displayed. 
# Finally, the registration page is rendered with the form.

def register(request):
    # Create an instance of the CreateUserForm
    form = CreateUserForm()

    # Check if the request method is POST
    if request.method == "POST":
        # Create an instance of the CreateUserForm with the POST data
        form = CreateUserForm(request.POST)
        # print(form)
        # Check if the form data is valid
        if form.is_valid():
            try:
                # Retrieve the username and email from the form data
                username = form.cleaned_data['username']
                to_email = form.cleaned_data['email']
                print(username, to_email)

                # Check if the username is already taken
                if User.objects.filter(username=username).first():
                    # Display a success message and redirect to the register page if the username is taken
                    messages.success(request, "username already taken")
                    return redirect("/register")

                # Check if the email is already taken
                if User.objects.filter(email=to_email).first():
                    # Display a success message and redirect to the register page if the email is taken
                    messages.success(request, "email taken.")
                    return redirect("/register")

                # Save the form data to create a new user, but don't activate the user yet
                user = form.save(commit=False)
                user.is_active = False
                
                
               
                user = form.save()
                group=Group.objects.get(name='user')
                user.groups.add(group)

                # Generate the verification email content
                uid = user.pk
                subject = "your account needs to be verified"
                message = f"hi, please press the link to verify: http://127.0.0.1:8000/verify/{uid}"

                # Send the verification email
                sent_mail_from(to_email, subject, message)

                # Display a success message and redirect to the register page
                messages.success(request, "verification email has been sent successfully. Please check your email and click the link for confirmation.")
                return redirect("/register")

            except Exception as e:
                print(e)
                # Return an error message if something goes wrong
                return HttpResponse("something went wrong")

        else:
            # Display the form validation errors if the form data is invalid
            messages.error(request, form.error_messages)

    # Prepare the context for rendering the registration page
    context = {"form": form}

    # Render the registration page with the context
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
            messages.success(request, "Request Submit Successfully ")
            return redirect("/dashboard")

    return render(request, "base/registration2.html", {"form2": form2})


def logoutpage(request):
    logout(request)
    return redirect("login")
