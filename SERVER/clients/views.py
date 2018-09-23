from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUP_Form, Register
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Devices, Patient
import datetime
from django.contrib.auth import logout



from.init_model import init_on_register
# Create your views here.


def HomePage(request):
    template_name = "pages/index.html"
    context = {}

    return render(request, template_name, context)

def Login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username= username, password= password)

        if user is not None:
            login(request, user)


            return redirect('/client/')

        else:

            template_name = "pages/signin.html"
            context = {'error' : "Please type the correct authentication details"}

            return render(request, template_name, context)


    else:

        template_name = "pages/signin.html"
        context = {}

        return render(request, template_name, context)


def SignUP(request):

    if request.method == "GET":
        form = SignUP_Form()
        template_name = "pages/signup.html"
        context = {"form" : form, "Name": "USER SIGNUP"}

        return render(request, template_name, context)

    elif request.method == "POST":


        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        User.objects.create_user(username=username, email=email, password= password)

        return redirect("/")


    else:

       messages.add_message(request, messages.ERROR, "The passwords didn't match")
       return redirect("/client/signup")


def Register_devices(request):

    if request.method == "GET":

        form = Register()
        template_name = "pages/add_devices.html"
        context = {"form": form, "Name": "DEVICES"}

        return render(request, template_name, context)


    else:
        form = Register(request.POST)
        if form.is_valid():




            d = Devices()
            d.user = request.user

            p = form.cleaned_data["acess_token"]


            d.last_connected = datetime.datetime.now()
            d.device_id = form.cleaned_data["device_id"]
            d.save()


            return  redirect("/client")
        else:
            form = Register()
            template_name = "pages/add_devices.html"
            context = {"form": form, "Name": "DEVICES"}

            return render(request, template_name, context)

def Device_info(request):

    if request.method == "GET":

        user = request.user
        devices = Devices.objects.filter(user = user)
        d_id = []
        for i in devices:
            d_id.append(i)

        template_name = "pages/device_list.html"
        context = {"d_id" : d_id, "username": user.username}

        return render(request, template_name, context)


def Logout(request):

    logout(request)

    return redirect("/")


def Reset(request):
    pass





