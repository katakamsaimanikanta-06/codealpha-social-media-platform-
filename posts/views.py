from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils.timesince import timesince

from .models import Post, Like, Comment
from .forms import PostForm, CommentForm


def feed_view(request):
    """
    Main feed view. For authenticated users, supports 'following' tab (default)
    and 'explore' tab. Also handles top post composer form submission.
    """
    # 1. Handle Post Creation Form Submission (if authenticated)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Your post has been published!")
            return redirect('posts:feed')
        else:
            messages.error(request, "Failed to publish post. Please check your content.")
    else:
        form = PostForm()

    # 2. Determine feed tab & query posts
    tab = request.GET.get('tab', 'following' if request.user.is_authenticated else 'explore')
    query = request.GET.get('q', '').strip()

    posts_qs = Post.objects.select_related('author', 'author__profile').prefetch_related('likes', 'comments')

    if query:
        posts_qs = posts_qs.filter(
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )
    elif tab == 'following' and request.user.is_authenticated:
        following_ids = list(request.user.following_set.values_list('following_id', flat=True))
        # Include current user's posts too
        following_ids.append(request.user.id)
        posts_qs = posts_qs.filter(author_id__in=following_ids)

    # Pagination
    paginator = Paginator(posts_qs, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    # Cache user's liked post IDs for instant icon highlight
    user_liked_post_ids = set()
    if request.user.is_authenticated:
        user_liked_post_ids = set(request.user.likes.values_list('post_id', flat=True))

    context = {
        'form': form,
        'posts': posts,
        'tab': tab,
        'query': query,
        'user_liked_post_ids': user_liked_post_ids,
    }
    return render(request, 'posts/feed.html', context)


def post_detail_view(request, post_id):
    """
    Detailed single post view with full comment thread and comment submission form.
    """
    post = get_object_or_404(
        Post.objects.select_related('author', 'author__profile').prefetch_related('comments__author__profile', 'likes'),
        id=post_id
    )

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                avatar_url = comment.author.profile.avatar.url if comment.author.profile.avatar else None
                return JsonResponse({
                    'status': 'success',
                    'comment_id': comment.id,
                    'author_username': comment.author.username,
                    'author_name': comment.author.profile.display_name,
                    'author_avatar': avatar_url,
                    'content': comment.content,
                    'created_at': timesince(comment.created_at) + " ago",
                    'comments_count': post.comments.count(),
                })

            messages.success(request, "Comment posted!")
            return redirect('posts:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    user_liked_post_ids = set()
    if request.user.is_authenticated:
        user_liked_post_ids = set(request.user.likes.values_list('post_id', flat=True))

    context = {
        'post': post,
        'comment_form': comment_form,
        'user_liked_post_ids': user_liked_post_ids,
        'comments': post.comments.all(),
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit_view(request, post_id):
    """
    Edit an existing post (author only).
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('posts:post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'posts/post_edit.html', {'form': form, 'post': post})


@login_required
def post_delete_view(request, post_id):
    """
    Delete a post (author only).
    """
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully.")
        return redirect('posts:feed')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required
def like_toggle_view(request, post_id):
    """
    AJAX toggle to like or unlike a post.
    """
    post = get_object_or_404(Post, id=post_id)
    like_rel = Like.objects.filter(user=request.user, post=post)

    if like_rel.exists():
        like_rel.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes_count': post.likes.count(),
        })

    return redirect(request.META.get('HTTP_REFERER', 'posts:feed'))


@login_required
def comment_delete_view(request, comment_id):
    """
    Delete a comment (by comment author or post author).
    """
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user == comment.post.author:
        post_id = comment.post.id
        comment.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'message': "Comment deleted."})
        messages.info(request, "Comment deleted.")
        return redirect('posts:post_detail', post_id=post_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': "Unauthorized."}, status=403)
    messages.error(request, "You do not have permission to delete this comment.")
    return redirect('posts:feed')
