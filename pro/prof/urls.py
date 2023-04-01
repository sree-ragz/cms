from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_view
from . import views
urlpatterns = [
    path('',views.index,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('reviewertable/',views.reviewertable,name='reviewertable'),
    path('registeredevents/',views.registeredevents,name='registeredevents'),
    path('submitedpaper/',views.submitedpaper,name='submitedpaper'),
    path('submitedposter/',views.submitedposter,name='submitedposter'),
    path('viewsubmitedpaper/<int:id>',views.viewsubmitedpaper,name='viewsubmitedpaper'),
    path('viewsubmitedposter/<int:id>',views.viewsubmitedposter,name='viewsubmitedposter'),
    path('reviewerposterpage/<int:id>',views.reviewerposterpage,name='reviewerposterpage'),
    path('reviewerpaperpage/<int:id>',views.reviewerpaperpage,name='reviewerpaperpage'),
    path('register_as_participant/<int:event_id>',views.register_as_participant,name='register_as_participant'),
    path('eventregistration/<int:event_id>',views.eventregistration,name='eventregistration'),
    path('register/',views.register,name='register'),
    path('register2/',views.register2,name='register2'),
    path('login/',views.loginpage,name='login'),
    path('logout/',views.logoutpage,name='logout'),
    path('token/',views.token_sent,name='token_sent'),
    path('verify/<uid>',views.verify,name='verify'),
    path('settings/',views.Editprofile,name='settings'),
    path('reset_password/',auth_view.PasswordResetView.as_view(template_name='forgetpassword.html'),name='reset_password'),
    path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='changepassword.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_confirm.html'),name='password_reset_complete'),
    path('admin_page/',views.admin_page,name='admin_page'),
    path('admin_event_list/',views.admin_event_list,name='admin_event_list'),
    path('admin_edit_event/<int:id>',views.admin_edit_event,name='admin_edit_event'),
    path('admin_delete_event/<int:id>',views.admin_delete_event,name='admin_delete_event'),
     path('admin_reviewer_paper',views.admin_reviewer_paper,name='admin_reviewer_paper'),
        path('admin_edit_reviewer_paper/<int:id>',views.admin_edit_reviewer_paper,name='admin_edit_reviewer_paper'),
        path('admin_delete_reviewer_paper/<int:id>',views.admin_delete_reviewer_paper,name='admin_delete_reviewer_paper'),
        path('admin_reviewer_poster',views.admin_reviewer_poster,name='admin_reviewer_poster'),
        path('admin_edit_reviewer_poster/<int:id>',views.admin_edit_reviewer_poster,name='admin_edit_reviewer_poster'),
        path('admin_delete_reviewer_poster/<int:id>',views.admin_delete_reviewer_poster,name='admin_delete_reviewer_poster'),
       path('admin_add_reviewer/',views.admin_add_reviewer,name='admin_add_reviewer'),
       path('admin_delete_reviewer/<str:name>',views.admin_delete_reviewer,name='admin_delete_reviewer'),

    
]
