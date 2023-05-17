from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_view
from .views import base_view,admin_view,login_and_signup_view,reviewer_view,user_view,chair_and_cochair

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
     path('reviewer_camera_ready_paper/<int:id>',reviewer_view.reviewer_camera_ready_paper,name='reviewer_camera_ready_paper'),
 path('reviewer_camera_ready_poster/<int:id>',reviewer_view.reviewer_camera_ready_poster,name='reviewer_camera_ready_poster'),
 path('reviewer_camera_ready_context/<int:id>',reviewer_view.reviewer_camera_ready_context,name='reviewer_camera_ready_context'),
    path('reviewerpaperpage/<int:id>',reviewer_view.reviewerpaperpage,name='reviewerpaperpage'),
    path('reviewercontextpage/<int:id>',reviewer_view.reviewercontextpage,name='reviewercontextpage'),
   
    path('register_as_participant/<int:event_id>',user_view.register_as_participant,name='register_as_participant'),
    path('eventregistration/<int:event_id>',user_view.eventregistration,name='eventregistration'),
    path('user_context_registration/<int:event_id>',user_view.user_context_registration,name='user_context_registration'),
    path('camera_ready_paper_submition/<int:paper_id>',user_view.camera_ready_paper_submition,name='camera_ready_paper_submition'),
    path('camera_ready_poster_submition/<int:id>',user_view.camera_ready_poster_submition,name='camera_ready_poster_submition'),
    path('camera_ready_context_submition/<int:id>',user_view.camera_ready_context_submition,name='camera_ready_context_submition'),
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
        path('admin_delete_chair_cochair/<str:name>',admin_view.admin_delete_chair_cochair,name='admin_delete_chair_cochair'),

     path('admin_reviewer_context/',admin_view.admin_reviewer_context,name='admin_reviewer_context'),
      path('admin_edit_reviewer_context/<int:id>',admin_view.admin_edit_reviewer_context,name='admin_edit_reviewer_context'),
        path('admin_delete_reviewer_context/<int:id>',admin_view.admin_delete_reviewer_context,name='admin_delete_reviewer_context'),
          path('admin_add_chair_and_cochair',admin_view.admin_add_chair_and_cochair,name='admin_add_chair_and_cochair'),
          path('admin_edit_paperpage/<int:id>',admin_view.admin_edit_paperpage,name='admin_edit_paperpage'),
          path('admin_edit_posterpage/<int:id>',admin_view.admin_edit_posterpage,name='admin_edit_posterpage'),
          path('admin_edit_contextpage/<int:id>',admin_view.admin_edit_contextpage,name='admin_edit_contextpage'),



             path('chair_view',chair_and_cochair.chair_view,name='chair_view'),
               path('chair_details/<int:id>',chair_and_cochair.chair_details,name='chair_details'),
                path('chair_edit_event/<int:id>',chair_and_cochair.chair_edit_event,name='chair_edit_event'),
                 path('registered_users',chair_and_cochair.registered_users,name='registered_users'),
                 path('chair_paper/<int:id>',chair_and_cochair.chair_paper,name='chair_paper'),
                  path('chair_paper_details/<int:id>',chair_and_cochair.chair_paper_details,name='chair_paper_details'),
                   path('chair_camera_ready_paper/<int:id>',chair_and_cochair.chair_camera_ready_paper,name='chair_camera_ready_paper'),
             path('chair_poster/<int:id>',chair_and_cochair.chair_poster,name='chair_poster'),
               path('chair_poster_details/<int:id>',chair_and_cochair.chair_poster_details,name='chair_poster_details'),
                    path('chair_camera_ready_poster/<int:id>',chair_and_cochair.chair_camera_ready_poster,name='chair_camera_ready_poster'),
                   path('chair_context/<int:id>',chair_and_cochair.chair_context,name='chair_context'),
                    path('chair_context_details/<int:id>',chair_and_cochair.chair_context_details,name='chair_context_details'),
                    path('chair_camera_ready_context/<int:id>',chair_and_cochair.chair_camera_ready_context,name='chair_camera_ready_context'),
                     path('admin_registered_user',admin_view.admin_registered_user,name='admin_registered_user'),
                     path('admin_activate_deactivate_user/<int:id>',admin_view.admin_activate_deactivate_user,name='admin_activate_deactivate_user'),







                      path('cochair_view',chair_and_cochair.co_chair_view,name='cochair_view'),
                       path('cochair_details/<int:id>',chair_and_cochair.co_chair_details,name='cochair_details'),
                       path('cochair_edit_event/<int:id>',chair_and_cochair.co_chair_edit_event,name='cochair_edit_event'),
                       path('cochair_registered_users/<int:id>',chair_and_cochair.cochair_registered_users,name='cochair_registered_users'),
                        path('cochair_paper/<int:id>',chair_and_cochair.co_chair_paper,name='cochair_paper'),
                  path('cochair_paper_details/<int:id>',chair_and_cochair.co_chair_paper_details,name='cochair_paper_details'),
                  path('cochair_camera_ready_paper/<int:id>',chair_and_cochair.co_chair_camera_ready_paper,name='cochair_camera_ready_paper'),


                   path('cochair_poster/<int:id>',chair_and_cochair.co_chair_poster,name='cochair_poster'),
               path('cochair_poster_details/<int:id>',chair_and_cochair.co_chair_poster_details,name='cochair_poster_details'),
                    path('cochair_camera_ready_poster/<int:id>',chair_and_cochair.co_chair_camera_ready_poster,name='cochair_camera_ready_poster'),
                   path('cochair_context/<int:id>',chair_and_cochair.co_chair_context,name='cochair_context'),
                    path('cochair_context_details/<int:id>',chair_and_cochair.co_chair_context_details,name='cochair_context_details'),
                    path('cochair_camera_ready_context/<int:id>',chair_and_cochair.co_chair_camera_ready_context,name='cochair_camera_ready_context'),
                    
]

