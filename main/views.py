from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDoList, Item
from .forms import CreateNewList
# from .forms import NewUserForm
from django.contrib.auth import login, authenticate  # add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this


def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("Invalid input")

    return render(response, "main/list.html", {"ls": ls})


def home(response):
    return render(response, "main/home.html", {})


def create(response):

    if response.method == 'POST':
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data['name']
            t = ToDoList(name=n)
            t.save()

    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})
