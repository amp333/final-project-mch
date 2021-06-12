from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

#Creating my views here
def index(request):
    return render(request, 'index.html')

def welcome(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'crypto_messages': Crypto_Message.objects.all()
    }
    return render(request, 'welcome.html', context)
  
def register(request):
    print(request.POST)
   
    errors = User.objects.basic_validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    new_user = User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=request.POST['Password'])
    request.session['user'] = new_user.first_name
    request.session['id'] = new_user.id
    return redirect('/welcome')

def login(request):
    print(request.POST)

    logged_user = User.objects.filter(email=request.POST['email'])
    if len(logged_user) > 0:
        logged_user = logged_user[0]
        if logged_user.password == request.POST['Password']:
            request.session['user'] = logged_user.first_name
            request.session['id'] = logged_user.id
            return redirect('/welcome')
    return redirect('/')

def logout(request):
    print(request.session)
    request.session.flush()
    print(request.session)
    return redirect('/')

def post_mess(request):
    Crypto_Message.objects.create(message=request.POST['mess'], poster=User.objects.get(id=request.session['id']))
    return redirect('/welcome')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['id'])
    message = Crypto_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, crypto_message=message)
    return redirect('/welcome')

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    liked_message = Crypto_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/welcome')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/welcome')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['fname']
    edit_user.last_name = request.POST['lname']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/welcome')


def single_user(request, user_id):
    user = User.objects.get(id = user_id)
    likes = user.likes.all()
    context = {
        'user': user,
        'likes': likes
    }
    return render(request, 'welcome.html', context)

