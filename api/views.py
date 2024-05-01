from django.shortcuts import render, redirect
import requests, json
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, SignUpForm

# Create your views here.

def get_user_name(request, data):
    if request.user.is_authenticated:
        data['login'] = False
        data['username'] = request.user.username

    else:
        data['login'] = True
    return data

@login_required
def get_upcoming_movies(request):
    url = "https://moviesdatabase.p.rapidapi.com/titles/x/upcoming"

    headers = {
	    "X-RapidAPI-Key": "0f089168c0msh3d960bdd3ef41f3p163734jsn76b9cbedbab8",
	    "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"  
    }

    movies_data = {}
    get_movies = False
    response = requests.get(url, headers=headers)

    response = response.json()
    if 'results' in response.keys():
        try:
            print("Intry")
            get_movies = True
            movies = open("movies_list.json", "w")
            movies_data = response["results"]
            json.dump(movies_data, movies)
        except:
            print(response)
            movies = open("movies_list.json", "r")
            movies_data = json.load(movies)
    else:
        print(response)
    data = {
        "login": False,
        "movies": movies_data,
        "get_movies": get_movies
    }
    data = get_user_name(request, data)
    return render(request, template_name="upcoming.html", context=data)

@login_required
def get_gener_based(request):
    param = request.GET.get('param')
    print("parmeter : ", param)
    querystring = {"gener":param,"limit":"10", "startYear": "2023"}

    url = "https://moviesdatabase.p.rapidapi.com/titles"

    headers = {
	"X-RapidAPI-Key": "0f089168c0msh3d960bdd3ef41f3p163734jsn76b9cbedbab8",
	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    querystring = {"startYear":"2021","limit":"10"}

    response = requests.get(url, headers=headers, params=querystring)

    response = response.json()
    if 'results' in response.keys():
        try:
            print("Intry")
            get_movies = True
            movies_data = response["results"]
            movies = open("movies_list.json", "w+")
            json.dump(movies_data, movies)
        except:
            print("in exception")
            print(response)
            movies = open("movies_list.json", "r")
            movies_data = json.load(movies)
    else:
        print(response)
    data = {
        "login": False,
        "movies": movies_data,
        "get_movies": get_movies
    }
    data = get_user_name(request, data)


    return render(request, template_name="index.html", context=data)




@login_required
def index(request):

    movies_data = {}
    get_movies = False


    url = "https://moviesdatabase.p.rapidapi.com/titles/random"

    headers = {
	"X-RapidAPI-Key": "0f089168c0msh3d960bdd3ef41f3p163734jsn76b9cbedbab8",
	"X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    querystring = {"startYear":"2022"}

    response = requests.get(url, headers=headers, params=querystring)

    response = response.json()
    if 'results' in response.keys():
        try:
            print("Intry")
            get_movies = True
            movies = open("movies_list.json", "w")
            movies_data = response["results"]
            json.dump(movies_data, movies)
        except:
            print(response)
            movies = open("movies_list.json", "r")
            movies_data = json.load(movies)
    else:
        print(response)
    data = {
        "login": False,
        "movies": movies_data,
        "get_movies": get_movies
    }
    data = get_user_name(request, data)

    return render(request, template_name="index.html", context=data)



def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:  # Ensure user object is valid
                login(request, user)  # Log in the user
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('index')  # Default redirect if 'next' parameter is not present
    else:
        form = UserLoginForm()

    return render(request, template_name='login.html', context={'form': form, 'login': False})



# views.py

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object
            login(request, user)  # Log in the user
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'login.html', context={'form': form, 'login': False})