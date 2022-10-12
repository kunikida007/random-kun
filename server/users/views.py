from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserCreationForm, LoginForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(to='common:home')
    else:
        form = UserCreationForm() 
    param = {
        'form': form
    }
    return render(request, 'users/signup.html', param)


class LoginView(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    
    
class LogoutView(LogoutView):
    template_name = 'common/home.html'
