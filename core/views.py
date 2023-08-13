from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import profile, post, likepost, followersCount
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = profile.objects.get(user=user_object)
    
    posts = post.objects.all()
    return render(request, 'index.html', {'user_profile' : user_profile, 'posts' : posts})

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user to setting
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create profile

                user_model = User.objects.get(username=username)
                new_profile = profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signin')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username , password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')
    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

def settings(request):
    user_profile = profile.objects.get(user = request.user)

    if request.method == 'POST':
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('settings')
    return render(request, 'setting.html', {'user_profile' : user_profile})

@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='signin')
def profile_page(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = profile.objects.get(user=user_object)
    user_posts = post.objects.filter(user=user_object)
    user_post_length = len(user_posts)
    
    follower = request.user.username
    user = pk

    if followersCount.objects.filter(follower=follower,user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(followersCount.objects.filter(user=pk))
    user_following = len(followersCount.objects.filter(follower=pk))

    context = {
        'user_object' : user_object,
        'user_profile' : user_profile,
        'user_posts' : user_posts,
        'user_post_length' : user_post_length,
        'button_text' : button_text,
        'user_followers' : user_followers,
        'user_following' : user_following,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post_instance = post.objects.get(id=post_id)

    like_filter = likepost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = likepost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post_instance.no_of_likes = post_instance.no_of_likes + 1
        post_instance.save()
        return redirect('/')
    else:
        like_filter.delete()
        post_instance.no_of_likes = post_instance.no_of_likes - 1
        post_instance.save()
        return redirect('/')
    
@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if followersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = followersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile_page/'+user)
        else:
            new_follower = followersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile_page/'+user)
    else:
        return redirect('/')