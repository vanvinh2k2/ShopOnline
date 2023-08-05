from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Profile

# Create your views here.
def register_view(request):
    
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, "Hi %s, You account was created successfully" \
                             %(form.cleaned_data.get('username')))
            new_user = authenticate(username=form.cleaned_data.get('email'), 
                                    password=form.cleaned_data.get('password1')
            )
            new_user.set_password(form.cleaned_data.get('password1'))
            login(request, new_user)

            Profile.objects.create(user=new_user)
            return redirect('core:index')

    else: form = UserRegisterForm()

    content = { "form" : form }
    return render(request, 'userauths/sign-up.html', content)

def login_view(request):
    content = {}
    if request.user.is_authenticated :
        redirect('core:index')

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else: messages.warning(request, "User doesn't exits!")
        except:
            messages.warning(request, "User with %s does not exits" %email)
        
    return render(request, 'userauths/login.html', content)

def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out.")
    return redirect("userauths:login")
