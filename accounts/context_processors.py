from django.contrib.auth.models import User
from .models import Follow


def social_context(request):
    """
    Context processor to provide suggested users to follow and trending tags.
    """
    suggested_users = []
    if request.user.is_authenticated:
        # Exclude self and users already followed
        following_ids = request.user.following_set.values_list('following_id', flat=True)
        suggested_users = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids).select_related('profile')[:5]
    else:
        suggested_users = User.objects.all().select_related('profile')[:5]

    trending_tags = [
        {'tag': '#WebDev', 'posts': '12.4K'},
        {'tag': '#DjangoPython', 'posts': '8.2K'},
        {'tag': '#NexusCreators', 'posts': '18.3K'},
        {'tag': '#AIandTech', 'posts': '24.1K'},
        {'tag': '#OpenSource', 'posts': '3.9K'},
    ]

    return {
        'suggested_users': suggested_users,
        'trending_tags': trending_tags,
    }
