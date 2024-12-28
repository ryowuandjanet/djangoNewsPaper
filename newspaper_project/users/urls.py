from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('signup/', views.signup, name='signup'),
  path('logout/', views.CustomLogoutView.as_view(), name='logout'),  
  path('verify-email/<str:token>/', views.verify_email, name='verify_email'),
  path('users/password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
         
    path('users/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
         
    path('users/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
         
    path('users/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
