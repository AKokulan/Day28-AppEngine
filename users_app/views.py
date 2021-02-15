from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users_app.forms import CustomRegisterForm
# Create your views here.

def register(request):
    if request.method =='POST':
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,("New User Account Created"))
            return redirect('register')

        else:
            register_form = CustomRegisterForm(request.POST)
            return render(request, 'register.html', {'register_form': register_form})

    else:
        if request.user.is_authenticated:
            #register_form=CustomRegisterForm()
            return HttpResponse('You are already logged in')
        else:
            register_form=CustomRegisterForm()
            return render(request,'register.html',{'register_form':register_form})
@login_required
def account(request):
   return render(request,'account.html',{})


