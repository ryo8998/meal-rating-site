from django.forms.widgets import EmailInput
from django.shortcuts import redirect, render
from django.views.generic import CreateView, View
from django.urls import reverse_lazy
from accounts.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
# Create your views here.

class SignUpView(View):

    def get(self,request):
        form = SignUpForm
        return render(request,"registration/signup.html",context={'form':form})

    def post(self,request):
        print(request.POST.get('username'))
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            User.objects.create_user(
                data['username'],data['email'],data['password1']
            )
            user = authenticate(request, username=data['username'], password=data['password1'])
            login(request,user)
        return redirect(to="index")