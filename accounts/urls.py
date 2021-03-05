from django.urls import path, include
from django.contrib.auth import views as av
from . import views
from .forms import CustomAuthenticationForm

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),

    path('login/', av.LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path('logout/', av.LogoutView.as_view(template_name='regstration/logged_out.html', next_page='/'), name='logout'),

    path('password_change/', av.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', av.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', av.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', av.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset///', av.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', av.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #path('create/', views.UserCreateView.as_view(), name="create"),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('change/', views.UserChangeView.as_view(), name="change"),
]