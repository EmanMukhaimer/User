from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from .forms import *

def index(request):
    
    return render(request, "index.html")

def register(request):
    if request.method == 'POST':
        if len(all_users())==0:
            rule="admin"
        else:
            rule="normal"
        form = RegisterForm(request.POST)
        information=[request.POST['first_name'],request.POST['last_name'],request.POST['email'], request.POST['password'], rule]
        if form.is_valid():
            if not error_reg(request):
                request.session['loged_in_user_id'] = register_new_user(information).id
                return redirect('/user_dashboard')
            else:
                return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['loged_in_user_id'] = filter_users_email(request.POST['email'])[0].id
            return redirect('/user_dashboard')
    else:
        form = LoginForm()
    return render(request, "signin.html", {'form': form})


def user_dashboard(request):
    if 'loged_in_user_id' in request.session:
        request.session['loged_in_user']= True
        
        users=all_users()
        return render(request, "user_dashboard.html", {'users':users, 'admins': check_if_users_is_admin(request.session['loged_in_user_id']) })
    return redirect('/')


def add_new(request):
    if request.method == 'POST':
        rule="Normal"   
        form = RegisterForm(request.POST)
        information=[request.POST['first_name'],request.POST['last_name'],request.POST['email'], request.POST['password'], rule]
        if form.is_valid():
            if not error_reg(request):
                register_new_user(information)
                return redirect('/user_dashboard')
            else:
                return render(request, 'creat_user.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'creat_user.html', {'form': form})


def delete_user(request, number):
    delete_user_from_model(number)
    return redirect('/user_dashboard')

def view_user(request,number):
    # Don't allow a user who is not logged in to reach the /success route (i.e. by making a GET request in the address bar)
    if 'loged_in_user_id' in request.session:
        context={
            'user':get_user(number),
            'messages':filter_messages_by_written_to(get_user(number)).order_by("-created_at") ,
            'comments': all_comments(),
        }
        return render(request, "user_page.html", context)
    return redirect("/")

def edit_user(request,number):
    # Don't allow a user who is not logged in to reach the /success route (i.e. by making a GET request in the address bar)
    if 'loged_in_user_id' in request.session and check_if_users_is_admin(request.session['loged_in_user_id']):
        context={
            'user':get_user(number),
            'admins': check_if_users_is_admin(request.session['loged_in_user_id'])
        }
        return render(request, "edit_user.html", context)
    return redirect("/")

def edit_loged_in_user(request):
    # Don't allow a user who is not logged in to reach the /success route (i.e. by making a GET request in the address bar)
    if 'loged_in_user_id' in request.session:
        context={
            'user':get_user(request.session['loged_in_user_id']),
            'admins': check_if_users_is_admin(request.session['loged_in_user_id'])
        }
        return render(request, "edit_user.html", context)
    return redirect("/")

def logout(request):
    request.session.clear()	
    return redirect('/')




def post_message(request,number):
    create_message(request)
    return redirect('view_user', number)

def post_comment(request,number):
    create_comment(request)
    return redirect('view_user', number)


def edit_information(request):
    id=request.POST['user']
    update_information([request.POST['email'],request.POST['first_name'], request.POST['last_name'], request.POST['rule']], id)
    return redirect('view_user', id)


def edit_loged_in_user_password(request):
    id=request.POST['user']
    if not update_password(request, id):
        return redirect('view_user', id)
    else:
        return redirect('users/edit/')


def edit_password(request):
    id=request.POST['user']
    if not update_password(request, id):
        return redirect('view_user', id)
    else:
        return redirect('edit_user', id)

def edit_description(request):
    id=request.POST['user']
    update_description(request.POST['description'], id)
    return redirect('view_user', id)

