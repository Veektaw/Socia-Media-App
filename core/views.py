from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile, Picturegram, PostLikes, Follow
from itertools import chain
import random


@login_required(login_url='signin')
def index(request):
    
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    user_following_feed_list = []
    user_follow_feed = []
    
    user_following = Follow.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_feed_list.append(users.user)
        
    for usernames in user_following_feed_list:
        feed_lists = Picturegram.objects.filter(user=usernames)
        user_follow_feed.append(feed_lists)
        
    feed_list = list(chain(*user_follow_feed))
    
    all_users = User.objects.all()
    all_users_following = []
    
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        all_users_following.append(user_list)
        
    new_suggestions = [i for i in list(all_users) if (i not in list(all_users_following))]
    current_user_in_database = User.objects.filter(username=request.user.username)
    end_suggesttions = [i for i in list(new_suggestions) if (i not in list(current_user_in_database))]
    
    random.shuffle(end_suggesttions)
    
    username_profile =[]
    username_profile_suggestions = []
    
    for users in end_suggesttions:
        username_profile.append(users.id)
        
    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user=ids)
        username_profile_suggestions.append(profile_list)
    
    
    suggestion_profile_list = list(chain(*username_profile_suggestions))
        
    
    return render(request, 'index.html', {'user_profile': user_profile, 'user_feed': feed_list, 'suggestion_profile_list': suggestion_profile_list[:4]})


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    
    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profile_image
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
            
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect ('settings')
            
            
    return render(request, 'setting.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def search(request):
    
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    
    
    
    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)
        
        username_profile = []
        users_profile_list = []
        
        for users in username_object:
            username_profile.append(users.id)
            
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            users_profile_list.append(profile_lists)
            
        users_profile_list = list(chain(*users_profile_list))
        
    return render(request, 'search.html', {'user_profile':user_profile,'users_profile_list': users_profile_list })    


@login_required(login_url='signin')
def follow(request):
    
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']
        
        if Follow.objects.filter(follower=follower, user=user).first():
            delete_follow = Follow.objects.filter(follower=follower, user=user)
            delete_follow.delete()
            return redirect('/profile/'+user)
            
        else:
            new_follow = Follow.objects.create(follower=follower, user=user)
            new_follow.save()
            return redirect('/profile/'+user)
        
    else:
        return redirect('/')


@login_required(login_url='signin')
def upload(request):
    
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('posted_images')
        caption = request.POST['caption']
        
        new_upload = Picturegram.objects.create(user=user, image=image, caption=caption)
        new_upload.save()
        
        return redirect('/')
        
    else:
        return redirect('/')


@login_required(login_url='signin')
def profile(request, pk):
    
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Picturegram.objects.filter(user=pk)
    posts_length = len(user_posts)
    
    follower = request.user.username
    user = pk
    
    if Follow.objects.filter(follower=follower, user=user).first():
        follow_button = 'UnFollow'
        
    else:
        follow_button = 'Follow'
        
        
    followers_count = len(Follow.objects.filter(user=pk))
    following_count = len(Follow.objects.filter(follower=pk))
    
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'posts_length': posts_length,
        'follow_button': follow_button,
        'followers_count': followers_count,
        'following_count': following_count
    }
    
    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def likes(request):
    
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Picturegram.objects.get(id=post_id)
    
    filter_likes = PostLikes.objects.filter(post_id=post_id, username=username).first()
    
    
    # Creates new like of the current user hasn't liked the picture
    if filter_likes == None:
        new_like = PostLikes.objects.create(post_id=post_id, username=username)
        new_like.save()
        
        # Increases number of likes
        post.like_count = post.like_count+1
        post.save()
        
        return redirect('/')
    
    else:
        filter_likes.delete()
        post.like_count = post.like_count-1
        post.save()
        
        return redirect('/')


def signup(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken ')
                return redirect('signup')
            
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save
                
                # Logs a user in upon signup
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                
                # Create a user profile which is redirected to the settings page
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                
                return redirect('settings')
                
                
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')
    
    
def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('signin')
        
    else:
        return render(request, 'signin.html')
    

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
