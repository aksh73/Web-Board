from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from .views import *

urlpatterns = [
    path('signup/', accounts_views.signup, name='signup'),
    path('password_change/done/',accounts_views.changed_done,name='changed_done'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html', email_template_name='registration/password_reset_email.html', subject_template_name='registration/password_reset_subject.txt'),name='password_reset'),
    path('password_reset/done/' ,auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),name='password_change'),
    path('settings/my_account/', accounts_views.UserUpdateView.as_view(), name='my_account'),
# path('reset-password/done/' ,accounts_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),

]
