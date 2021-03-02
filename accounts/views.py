from django.contrib.auth.forms import UserCreationForm
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
