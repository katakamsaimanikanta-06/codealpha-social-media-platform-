from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Profile, Follow
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from posts.models import Post


def register_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to Nexus, @{user.username}!")
            return redirect('posts:feed')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:feed')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, @{user.username}!")
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url if next_url else 'posts:feed')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'accounts/login.html', {'next': request.GET.get('next', '')})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


def profile_view(request, username):
    profile_user = get_object_or_404(User.objects.select_related('profile'), username=username)
    profile = profile_user.profile
    
    is_self = (request.user == profile_user)
    is_following = False
    if request.user.is_authenticated and not is_self:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    tab = request.GET.get('tab', 'posts')
    if tab == 'likes':
        # Posts liked by profile_user
        liked_post_ids = profile_user.likes.values_list('post_id', flat=True)
        posts = Post.objects.filter(id__in=liked_post_ids).select_related('author', 'author__profile').prefetch_related('likes', 'comments')
    else:
        posts = profile_user.posts.select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    # Get set of post IDs liked by the logged-in user
    user_liked_post_ids = set()
    if request.user.is_authenticated:
        user_liked_post_ids = set(request.user.likes.values_list('post_id', flat=True))

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'is_self': is_self,
        'is_following': is_following,
        'tab': tab,
        'posts': posts,
        'user_liked_post_ids': user_liked_post_ids,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('accounts:profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/profile_edit.html', {'u_form': u_form, 'p_form': p_form})


@login_required
def follow_toggle_view(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': "You cannot follow yourself."}, status=400)
        messages.warning(request, "You cannot follow yourself.")
        return redirect('accounts:profile', username=username)

    follow_rel = Follow.objects.filter(follower=request.user, following=target_user)
    if follow_rel.exists():
        follow_rel.delete()
        following = False
        msg = f"You unfollowed @{target_user.username}."
    else:
        Follow.objects.create(follower=request.user, following=target_user)
        following = True
        msg = f"You are now following @{target_user.username}!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'following': following,
            'followers_count': target_user.followers_set.count(),
            'message': msg
        })

    messages.info(request, msg)
    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


def followers_list_view(request, username):
    target_user = get_object_or_404(User, username=username)
    followers = target_user.followers_set.select_related('follower', 'follower__profile').all()
    
    # List of users followed by the current logged-in user
    current_following_ids = set()
    if request.user.is_authenticated:
        current_following_ids = set(request.user.following_set.values_list('following_id', flat=True))

    context = {
        'target_user': target_user,
        'follow_users': [f.follower for f in followers],
        'title': f"People following @{target_user.username}",
        'active_type': 'followers',
        'current_following_ids': current_following_ids,
    }
    return render(request, 'accounts/followers_list.html', context)


def following_list_view(request, username):
    target_user = get_object_or_404(User, username=username)
    following = target_user.following_set.select_related('following', 'following__profile').all()
    
    current_following_ids = set()
    if request.user.is_authenticated:
        current_following_ids = set(request.user.following_set.values_list('following_id', flat=True))

    context = {
        'target_user': target_user,
        'follow_users': [f.following for f in following],
        'title': f"People @{target_user.username} follows",
        'active_type': 'following',
        'current_following_ids': current_following_ids,
    }
    return render(request, 'accounts/followers_list.html', context)
