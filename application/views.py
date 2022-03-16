from django.shortcuts import render, redirect
from . models import User, Message, Comment
import bcrypt
from django.contrib import messages
from django.contrib.messages import get_messages

# Display Methods
def index(request):
    if 'user_id' in request.session:
        return redirect("/wall")
    else:
        return render(request, "index.html")

def wall(request):
    if 'user_id' in request.session:
        this_user = User.objects.get(id=request.session['user_id'])
        context = {
            'this_user': this_user,
            'all_messages': Message.objects.all().order_by("-created_at")
        }
        return render(request, "wall.html", context)
    else:
        return redirect("/")

# Action Methods
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            birthday = request.POST['birthday'],
            password = hash_pw
        )
        request.session['user_id'] = new_user.id
        return redirect("/")

def login(request):
    existing_user = User.objects.filter(email=request.POST['email']).first()
    errors = User.objects.login_validator(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")

    if existing_user is not None:
        if bcrypt.checkpw(request.POST['password'].encode(), existing_user.password.encode()):
            request.session['user_id'] = existing_user.id
            return redirect("/wall")
        else:
            print('password does not match')
            return redirect("/")
    else:
        return redirect("/")

def post_message(request):
    this_user = User.objects.get(id=request.session['user_id'])
    new_message = Message.objects.create(
        user = this_user,
        message = request.POST['message']
    )
    print(new_message)
    return redirect("/")

def post_comment(request):
    this_user = User.objects.get(id=request.session['user_id'])
    new_comment = Comment.objects.create(
        message = Message.objects.get(id=request.POST['message_id']),
        user = this_user,
        comment = request.POST['comment']
    )
    print(new_comment)
    return redirect("/")

def delete_comment(request, comment_id):
    this_comment = Comment.objects.get(id=comment_id)
    this_comment.delete()
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")