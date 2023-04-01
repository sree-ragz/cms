from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .models import *
from django.views.generic.edit import UpdateView
from django.core.mail import send_mail
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth import get_user_model
from datetime import date

# Create your views here.


def index(request):
    events = Event.objects.all()
    print(type(events.first().to_date))
    print(type(date.today()))
    print(events.first().to_date < date.today())


    return render(request, "homepage.html", {"events": events, "today": date.today()})


def admin_page(request):
    event = Event.objects.all().count()
    participant = Participant.objects.all().count()
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.all().count()
    poster = PosterSubmition.objects.all().count()

    return render(
        request,
        "admin_page.html",
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
        "admin_event_list.html",
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
    print(p.first().userid.username)

    form = AdminAddorEditReviewerPaper()
    if request.method == "POST":
        form = AdminAddorEditReviewerPaper(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("admin_reviewer_paper")

    return render(
        request,
        "admin_reviewer_paper.html",
        {"paper": paper, "form": form, "previllage": previllage, "reviewer": p,'ps':ps},
    )


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
        "admin_reviewer_poster.html",
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
        request, "reviewers.html", {"form": form, "previllage": previllage, "pre": pre}
    )


def admin_delete_reviewer(request, name):
    User.objects.filter(username=name).delete()
    return redirect("admin_add_reviewer")


@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            try:
                username = form.cleaned_data.get("username")
                to_email = form.cleaned_data.get("email")
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

                sent_mail_from(to_email, user)
                return redirect("token_sent")
                # login(request, user)
                # return redirect('register2')
            except Exception as e:
                return HttpResponse("something went wrong")
    context = {"form": form}
    return render(request, "registration.html", context)


def token_sent(request):
    return render(request, "token.html")


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

    return render(request, "registration2.html", {"form2": form2})


def dashboard(request):
    events = Event.objects.all()
    print(events)
    user = request.user
    previllage = Privillage.objects.filter(userid=request.user).first()

    participant_obj = Participant.objects.filter(user=user).first()

    return render(
        request,
        "dashboard.html",
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
                postersubmition.submit_count = 1
                postersubmition.save()

            return redirect("eventregistration", event_id)

        return render(
            request,
            "eventregistration.html",
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
        "profile.html",
        {
            "form": form,
            "participant_obj": participant_obj,
            
            
            "previllage": previllage,
        },
    )


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
            if user is not None:
                login(request, user)
                previllage = Privillage.objects.filter(userid=user).first()
                print(previllage.participant)
                if previllage.participant or previllage.is_author:
                    if participant_obj is None:
                        return redirect("/register2")
                    return redirect("dashboard")
                elif previllage.is_reviewer:
                    return redirect("reviewertable")
                elif previllage.is_admin:
                    return redirect("admin_page")

        except Exception as e:
            return HttpResponse("something went wrong")

    return render(request, "login.html")


def reviewertable(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    reviewerpaper = Reviewer_Paper.objects.filter(userid=request.user).all()
    reviewerposter = Reviewer_Poster.objects.filter(userid=request.user).all()
    return render(
        request,
        "reviewertable.html",
        {
            "reviewerpaper": reviewerpaper,
            "reviewerposter": reviewerposter,
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

            return redirect("reviewertable")

    return render(
        request,
        "reviewerposterpage.html",
        {"obj": poster, "form": form, "previllage": previllage},
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

            return redirect("reviewertable")

    return render(
        request,
        "reviewerpaperpage.html",
        {"obj": paper, "form": form, "previllage": previllage},
    )


def registeredevents(request):
    previllage = Privillage.objects.filter(userid=request.user).first()

    userevent = User_Event.objects.filter(user_id=request.user).all()

    return render(
        request, "registeredevents.html", {"event": userevent, "previllage": previllage}
    )


def submitedpaper(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    paper = PaperSubmition.objects.filter(userid=request.user).all()

    return render(
        request, "submitedpaper.html", {"paper": paper, "previllage": previllage}
    )


def submitedposter(request):
    previllage = Privillage.objects.filter(userid=request.user).first()
    poster = PosterSubmition.objects.filter(userid=request.user).all()

    return render(
        request, "submitedposter.html", {"poster": poster, "previllage": previllage}
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
        "viewsubmitedpaper.html",
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
        "viewsubmitedposter.html",
        {"poster": poster, "form": form, "previllage": previllage},
    )


def logoutpage(request):
    logout(request)
    return redirect("login")


def sent_mail_from(email, user):
    print(user.pk)
    print(user.id)
    uid = user.pk
    subject = "your account need to be verified"
    message = f"hi press the link to verify http://127.0.0.1:8000/verify/{uid}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
