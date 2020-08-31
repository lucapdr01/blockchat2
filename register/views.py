from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile


# function to get user ip
def getIp(request):
    try:
        x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward:
            ip = x_forward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ""
    return ip


# function to handle register form
def register(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)

        # Hidden form
        profileForm = UserProfileForm(request.POST)

        if form.is_valid() and profileForm.is_valid():

            user = form.save()
            profile = profileForm.save(commit=False)

            profile.user = user

            profile.save()

            return redirect("home")
    else:
        # initialise blank form and ip info
        form = RegisterForm()
        profileForm = UserProfileForm(initial={'ipAddress': getIp(request)})

    # render the page
    return render(request, "register/register.html", {"form": form, "profileForm": profileForm})


# handle logout
def logoutReq(request):
    logout(request)
    messages.info(request, "Logged out")
    return redirect("/")


# handle login
def loginReq(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            # Update user ip
            try:
                ip = UserProfile.objects.get(user=user)
                ip.value = getIp(request)
                ip.save()
            except:
                print("SuperUser")

            if user is not None:

                login(request, user)
                messages.success(request, "Successfully Logged in")
                return redirect('/')
            else:
                return render(request, "register/login.html", {"form": form})
        else:
            return render(request, "register/login.html", {"form": form})

    form = AuthenticationForm()
    return render(request, "register/login.html", {"form": form})


