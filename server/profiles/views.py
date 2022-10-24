from django.shortcuts import render
from django.views.generic import CreateView, TemplateView

from .forms import Profile


class ProfileCreateView(CreateView):
    form_class = Profile
    template_name = ""
    

class ProfileView(TemplateView):
    
