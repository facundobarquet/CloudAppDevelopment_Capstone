from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from .restapis import *

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
#testing view
def testNLU(request):
     if request.user:
        params = dict()
        text = "This is a test text!"
        result = analyze_review_sentiments(text) + "User" + str(request.user)
        return HttpResponse(result)



# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {
        "page":"about"
    }
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {
        "page":"contact"
    }
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request, page):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            url = 'djangoapp:'+page
            try:
                login(request, user)
                return redirect(url)
            except:
                url = 'djangoapp/'+page+'.html'
                context ={
                "error":"Wrong username or password"
                }
                return render(request, url, context)
        else:
            url = 'djangoapp/'+page+'.html'
            context ={
                "error":"Couldn't authenticate user"
            }
            return render(request, url, context)
    else:
        url = 'djangoapp/'+page+'.html'
        return render(request, url, context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request, page):
    context = {}
    if request.method == "GET":
        logout(request)
        url = 'djangoapp:'+ page
        return redirect(url)

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context = {
                "error" : "User already exists"
            }
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {
        "page":"index"
    }
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request,'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {
        "page":"index"
    }
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/faa4e27a-4308-4e63-99f9-80ea8ab01d4f/dealership-package/get-review-by-dealership.json"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        print(reviews)
        # Concat all dealer's short name
        #review_dealership = ' '.join([review.dealership for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(reviews)
    elif request.method == "POST":
        add_review(request, dealer_id)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    user = request.user
    if user.is_authenticated():
        review = request.body
        json_payload = {}
        json_payload["review" : review]
        result = post_request(url, json_payload, dealerId=dealer_id)
        print(result)
        return HttpResponse(result)