from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_view
from .views import base_view,admin_view,login_and_signup_view,reviewer_view,user_view

urlpatterns = [
    path('',base_view.index,name='home'),



    path('dashboard/',user_view.dashboard,name='dashboard'),
    path('reviewertable/',reviewer_view.reviewertable,name='reviewertable'),
    path('registeredevents/',user_view.registeredevents,name='registeredevents'),
    path('submitedpaper/',user_view.submitedpaper,name='submitedpaper'),
    path('submitedposter/',user_view.submitedposter,name='submitedposter'),
    path('submitedcontext/',user_view.submitedcontext,name='submitedcontext'),
    path('viewsubmitedpaper/<int:id>',user_view.viewsubmitedpaper,name='viewsubmitedpaper'),
    path('viewsubmitedposter/<int:id>',user_view.viewsubmitedposter,name='viewsubmitedposter'),
    path('viewsubmitedcontext/<int:id>',user_view.viewsubmitedcontext,name='viewsubmitedcontext'),
    path('reviewerposterpage/<int:id>',reviewer_view.reviewerposterpage,name='reviewerposterpage'),


    path('reviewerpaperpage/<int:id>',reviewer_view.reviewerpaperpage,name='reviewerpaperpage'),
    path('reviewercontextpage/<int:id>',reviewer_view.reviewercontextpage,name='reviewercontextpage'),
   
    path('register_as_participant/<int:event_id>',user_view.register_as_participant,name='register_as_participant'),
    path('eventregistration/<int:event_id>',user_view.eventregistration,name='eventregistration'),
    path('user_context_registration/<int:event_id>',user_view.user_context_registration,name='user_context_registration'),
    
    
    path('register/',login_and_signup_view.register,name='register'),
    path('register2/',login_and_signup_view.register2,name='register2'),



    path('login/',login_and_signup_view.loginpage,name='login'),
    path('logout/',login_and_signup_view.logoutpage,name='logout'),
    path('token/',login_and_signup_view.token_sent,name='token_sent'),
    path('verify/<uid>',login_and_signup_view.verify,name='verify'),
    path('settings/',user_view.Editprofile,name='settings'),
    path('reset_password/',auth_view.PasswordResetView.as_view(template_name='base/forgetpassword.html'),name='reset_password'),
    path('reset_password_sent/',auth_view.PasswordResetDoneView.as_view(template_name='base/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='base/changepassword.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='base/password_reset_confirm.html'),name='password_reset_complete'),
    path('admin_page/',admin_view.admin_page,name='admin_page'),
    path('admin_event_list/',admin_view.admin_event_list,name='admin_event_list'),
    path('admin_edit_event/<int:id>',admin_view.admin_edit_event,name='admin_edit_event'),
    path('admin_delete_event/<int:id>',admin_view.admin_delete_event,name='admin_delete_event'),
     path('admin_reviewer_paper',admin_view.admin_reviewer_paper,name='admin_reviewer_paper'),
        path('admin_edit_reviewer_paper/<int:id>',admin_view.admin_edit_reviewer_paper,name='admin_edit_reviewer_paper'),
        path('admin_delete_reviewer_paper/<int:id>',admin_view.admin_delete_reviewer_paper,name='admin_delete_reviewer_paper'),
        path('admin_reviewer_poster',admin_view.admin_reviewer_poster,name='admin_reviewer_poster'),
        path('admin_edit_reviewer_poster/<int:id>',admin_view.admin_edit_reviewer_poster,name='admin_edit_reviewer_poster'),
        path('admin_delete_reviewer_poster/<int:id>',admin_view.admin_delete_reviewer_poster,name='admin_delete_reviewer_poster'),
       path('admin_add_reviewer/',admin_view.admin_add_reviewer,name='admin_add_reviewer'),
       path('admin_delete_reviewer/<str:name>',admin_view.admin_delete_reviewer,name='admin_delete_reviewer'),

     path('admin_reviewer_context/',admin_view.admin_reviewer_context,name='admin_reviewer_context'),
      path('admin_edit_reviewer_context/<int:id>',admin_view.admin_edit_reviewer_context,name='admin_edit_reviewer_context'),
        path('admin_delete_reviewer_context/<int:id>',admin_view.admin_delete_reviewer_context,name='admin_delete_reviewer_context'),
]
