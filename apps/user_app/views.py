from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages

import bcrypt


# Create your views here.
def index(request):
    request.session['errors'] = []
    return render(request, "user_app/index.html")

def signin(request):
    return render(request, "user_app/signin.html")

def register(request):
    context = {
        "user_level" : "Normal"
    }
    return render(request, "user_app/register.html", context)

def user_create(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    response = User.objects.validate_registration_data(request.POST)

    if (response['status']):
        request.session['errors']  = []
        if 'user_id' in request.session:
            # this user is being created by an admin
            return redirect('/manage')
        else:
            # no users logged in (i.e. not being created by an admin)
            request.session['name']    = response['user'].first_name
            request.session['user_id'] = response['user'].id
            return redirect('/welcome')
    else:
        request.session['errors'] = response['errors']
        return redirect('/register')


def welcome(request):
    return render(request, "user_app/welcome.html")

def manage(request):
    this_user = User.objects.get(id=request.session['user_id'])

    context = {
        'users' : User.objects.all(),
        'this_users_level' : this_user.user_level
    }
    return render(request, "user_app/manage.html", context)

def admin_add_new(request):
    this_user = User.objects.get(id=request.session['user_id'])
    if this_user.user_level == "Admin":
        context = {
            "user_level" : this_user.user_level
        }
        return render(request, "user_app/register.html", context)
    else:
        messages.error(request, 'Sorry, you do not have privileges to add a user. Please contact an admin')
        context = {
            "messages" : messages.get_messages(request)
        }

        return render(request, "user_app/welcome.html", context)


def user_login(request):
    
    # the method validate_registration_data validates the form data and if there
    # are no errors, it also creates the user and returns the user object.
    # if there are errors, it returns a list of them in the response object.

    response = User.objects.validate_login_data(request.POST)

    if (response['status']):
        request.session['name']    = response['user'].first_name
        request.session['user_id'] = response['user'].id
        request.session['errors']  = []
        return redirect('/welcome')
    else:
        request.session['errors'] = response['errors']
        return redirect('/signin')

def user_logout(request):
    request.session['name'] = ""
    request.session['user_id'] = ""
    return redirect('/')

def edit(request, user_id):

    # displays the edit form using the id in the get request
    user = User.objects.get(id=user_id)
    context = {
        'user_id'   : user_id,
        'first_name': user.first_name,
        'last_name' : user.last_name,
        'email'     : user.email,
        'created_at': user.created_at
    }
    return render(request, "user_app/edit.html", context)

