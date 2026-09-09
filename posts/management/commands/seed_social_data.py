import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from PIL import Image, ImageDraw

from accounts.models import Profile, Follow
from posts.models import Post, Like, Comment


def generate_image(path, text, bg_color=(99, 102, 241), size=(600, 400)):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img = Image.new('RGB', size, color=bg_color)
    draw = ImageDraw.Draw(img)
    w, h = size
    draw.rectangle([10, 10, w - 10, h - 10], outline=(255, 255, 255, 60), width=2)
    draw.ellipse([w*0.1, h*0.1, w*0.9, h*0.9], outline=(255, 255, 255, 30), width=3)
    draw.text((w // 2, h // 2), text, fill=(255, 255, 255), anchor="mm")
    img.save(path, 'JPEG', quality=90)


class Command(BaseCommand):
    help = 'Seeds initial social media demo users, posts, follows, comments, and likes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding social media platform database..."))

        # 1. Admin Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@pulse.com',
                'first_name': 'CodeAlpha',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_profile, _ = Profile.objects.get_or_create(user=admin_user)
            admin_profile.bio = "Official Administrator of the Pulse Social Platform."
            admin_profile.location = "Global HQ"
            admin_profile.save()
            self.stdout.write(self.style.SUCCESS("Superuser 'admin' created."))

        # 2. Demo Users Data
        users_data = [
            {
                'username': 'alex_tech',
                'first_name': 'Alex',
                'last_name': 'Rivera',
                'email': 'alex@codealpha.com',
                'bio': 'Full-Stack Software Engineer & Python enthusiast. Building scalable web architectures and open-source tools. 💻⚡',
                'location': 'San Francisco, CA',
                'website': 'https://github.com',
                'avatar_color': (79, 70, 229),
            },
            {
                'username': 'sarah_design',
                'first_name': 'Sarah',
                'last_name': 'Chen',
                'email': 'sarah@codealpha.com',
                'bio': 'Senior Product Designer & UI/UX specialist. Passionate about typography, clean minimalism, and accessible web experiences. ✨🎨',
                'location': 'New York, NY',
                'website': 'https://dribbble.com',
                'avatar_color': (219, 39, 119),
            },
            {
                'username': 'marcus_ai',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'email': 'marcus@codealpha.com',
                'bio': 'AI/ML Researcher working on agentic workflows and transformer architectures. Coffee lover and tech tinkerer. 🤖☕',
                'location': 'Seattle, WA',
                'website': 'https://arxiv.org',
                'avatar_color': (13, 148, 136),
            },
            {
                'username': 'emma_travel',
                'first_name': 'Emma',
                'last_name': 'Watson',
                'email': 'emma@codealpha.com',
                'bio': 'Photographer, explorer & storyteller. Capturing everyday beauty and quiet moments around the globe. 📸✈️',
                'location': 'London, UK',
                'website': 'https://instagram.com',
                'avatar_color': (217, 119, 6),
            },
        ]

        user_objs = {}
        for u in users_data:
            user, u_created = User.objects.get_or_create(
                username=u['username'],
                defaults={
                    'first_name': u['first_name'],
                    'last_name': u['last_name'],
                    'email': u['email'],
                }
            )
            if u_created:
                user.set_password('password123')
                user.save()

            # Profile avatar
            av_rel = f"avatars/{u['username']}.jpg"
            av_abs = os.path.join(settings.MEDIA_ROOT, av_rel)
            if not os.path.exists(av_abs) or os.path.getsize(av_abs) == 0:
                generate_image(av_abs, u['first_name'][0], bg_color=u['avatar_color'], size=(300, 300))

            profile, _ = Profile.objects.get_or_create(user=user)
            profile.bio = u['bio']
            profile.location = u['location']
            profile.website = u['website']
            profile.avatar = av_rel
            profile.save()

            user_objs[u['username']] = user

        self.stdout.write(self.style.SUCCESS("Users and profiles created."))

        # 3. Follow Relationships
        follow_pairs = [
            ('alex_tech', 'sarah_design'),
            ('alex_tech', 'marcus_ai'),
            ('sarah_design', 'alex_tech'),
            ('sarah_design', 'emma_travel'),
            ('marcus_ai', 'alex_tech'),
            ('marcus_ai', 'sarah_design'),
            ('emma_travel', 'sarah_design'),
            ('emma_travel', 'alex_tech'),
        ]

        for follower_u, following_u in follow_pairs:
            Follow.objects.get_or_create(
                follower=user_objs[follower_u],
                following=user_objs[following_u]
            )

        self.stdout.write(self.style.SUCCESS("Follow relationships established."))

        # 4. Posts Data
        posts_data = [
            {
                'author': 'alex_tech',
                'content': "Just wrapped up building our new full-stack social web app with Django and Tailwind CSS! The speed of server-rendered templates combined with smooth AJAX interactivity is pure developer bliss. What's your favorite web stack in 2026? 🚀 #WebDev #DjangoPython",
                'image_text': 'Django + Tailwind Architecture',
                'image_color': (79, 70, 229),
            },
            {
                'author': 'sarah_design',
                'content': "Design tip of the day: Good UI is invisible. When the typography scale is balanced and the whitespace gives elements breathing room, users naturally glide through your product without friction. ✨ Less is always more. #DesignTips #UXUI",
                'image_text': 'Clean UI Design Principles',
                'image_color': (219, 39, 119),
            },
            {
                'author': 'marcus_ai',
                'content': "Autonomous coding agents are evolving at an extraordinary pace. The transition from simple text completion to multi-turn plan-and-execute workflows is fundamentally reshaping how we write and review software. Exciting times ahead! 🤖💡 #AIandTech",
                'image_text': 'Agentic AI Workflows',
                'image_color': (13, 148, 136),
            },
            {
                'author': 'emma_travel',
                'content': "Golden hour in the highlands. There is something truly grounding about leaving notifications behind and watching the fog drift across the valleys. Remember to take a break and step outside today! 🏔️✨ #TravelPhotography",
                'image_text': 'Mountain Golden Hour',
                'image_color': (217, 119, 6),
            },
            {
                'author': 'alex_tech',
                'content': "Tip: Always keep database operations atomic when processing mission-critical transactions. Django's `transaction.atomic()` decorator saves hours of debugging headaches! #Python #Database",
                'image_text': None,
                'image_color': None,
            },
        ]

        post_objs = []
        for i, p_info in enumerate(posts_data):
            img_rel = None
            if p_info['image_text']:
                img_rel = f"posts/post_{i+1}.jpg"
                img_abs = os.path.join(settings.MEDIA_ROOT, img_rel)
                if not os.path.exists(img_abs) or os.path.getsize(img_abs) == 0:
                    generate_image(img_abs, p_info['image_text'], bg_color=p_info['image_color'], size=(800, 450))

            post, _ = Post.objects.get_or_create(
                author=user_objs[p_info['author']],
                content=p_info['content'],
                defaults={'image': img_rel}
            )
            post_objs.append(post)

        self.stdout.write(self.style.SUCCESS("Posts created."))

        # 5. Likes
        # Like post 0 by Sarah, Marcus, Emma
        Like.objects.get_or_create(user=user_objs['sarah_design'], post=post_objs[0])
        Like.objects.get_or_create(user=user_objs['marcus_ai'], post=post_objs[0])
        Like.objects.get_or_create(user=user_objs['emma_travel'], post=post_objs[0])
        
        # Like post 1 by Alex, Marcus
        Like.objects.get_or_create(user=user_objs['alex_tech'], post=post_objs[1])
        Like.objects.get_or_create(user=user_objs['marcus_ai'], post=post_objs[1])

        # Like post 2 by Alex, Sarah
        Like.objects.get_or_create(user=user_objs['alex_tech'], post=post_objs[2])
        Like.objects.get_or_create(user=user_objs['sarah_design'], post=post_objs[2])

        # 6. Comments
        comments_data = [
            (post_objs[0], 'sarah_design', "Couldn't agree more! The crispness of server templates with Tailwind makes prototyping lightning fast."),
            (post_objs[0], 'marcus_ai', "Awesome work Alex! Are you leveraging SQLite with WAL mode for local concurrency?"),
            (post_objs[1], 'alex_tech', "Love this rule of thumb. Whitespace makes all the difference in modern web apps."),
            (post_objs[2], 'sarah_design', "The UX of interacting with intelligent agents is one of the most fascinating design frontiers right now."),
            (post_objs[3], 'emma_travel', "Breathtaking view! Where was this shot taken?"),
        ]

        for p, comment_author, content in comments_data:
            Comment.objects.get_or_create(
                post=p,
                author=user_objs[comment_author],
                content=content
            )

        self.stdout.write(self.style.SUCCESS("Likes and comments seeded successfully!"))
