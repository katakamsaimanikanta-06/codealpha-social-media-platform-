# ⚡ Pulse - Mini Social Media Platform

A full-stack, responsive modern mini Social Media web application built with **Django**, **SQLite**, **HTML5**, **CSS3 (Tailwind)**, and **JavaScript (AJAX)**.

---

## ✨ Key Features

- **👤 User Profiles & Authentication**:
  - Secure registration, sign-in, and sign-out with instant flash toasts.
  - Profile customization: Avatar upload, Cover header image, Display name, Bio, Location, and Website.
  - Follower count, Following count, and Posts count.
  - Tabbed profile views: **User Posts** and **Liked Posts**.

- **📝 Post Management (CRUD)**:
  - **Create**: Top composer card with text input, image attachment preview, and instant publish.
  - **View**: Responsive feed cards and dedicated single-post thread views.
  - **Edit**: Post owners can edit post text and replace images.
  - **Delete**: Post owners can delete their own posts with a confirmation prompt.

- **❤️ Social Interactivity**:
  - **Like / Unlike (AJAX)**: Instant heart toggle with bounce micro-animation and live counter without page refresh.
  - **Comments (AJAX)**: Post comments in real-time, view timestamped comment threads with author avatars, and allow authors to delete comments.
  - **Follow / Unfollow (AJAX)**: Instant follow button on profiles, suggested user cards, and followers lists.
  - **Followers & Following Lists**: Dedicated views showing follower/following user cards with follow toggles.

- **📰 Smart Feeds**:
  - **Following Feed (Home)**: Chronological stream of posts from creators you follow + your own posts.
  - **Explore Feed (Discover)**: Global stream of all posts across the community to discover new creators.
  - **Search**: Search bar filtering posts by content, hashtag, or author username.

- **🎨 Modern 3-Column UI Layout**:
  - **Left Sidebar**: Brand logo, Navigation links (Home, Explore, My Profile, Edit Profile, Admin Panel, Sign Out).
  - **Center Feed**: Sticky header, Post Composer, Tab Switcher, and Post stream.
  - **Right Sidebar**: Search bar, "Who to Follow" recommendations widget, and Trending Topics.
  - **Mobile**: Responsive bottom navigation bar and mobile top header.

- **🌱 Automated Seed Data**:
  - Single command `python manage.py seed_social_data` populates 5 realistic users, avatars, posts with imagery, follow relationships, likes, and comment threads out of the box!

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13+, Django 6.1+
- **Database**: SQLite3
- **Frontend**: HTML5, Tailwind CSS (via CDN), Custom CSS, Vanilla JavaScript (AJAX)
- **Icons & Typography**: Lucide Icons, Google Inter font
- **Image Processing**: Pillow

---

## 🚀 Getting Started & Local Setup

### 1. Prerequisites
Ensure you have **Python 3.10+** installed.

### 2. Navigate to the Project Directory
```powershell
cd C:\Users\megha\.gemini\antigravity\scratch\social_media_platform
```

### 3. Install Dependencies
```powershell
python -m pip install django pillow
```

### 4. Apply Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Demo Users, Posts & Relationships
Run the automated seed command:
```powershell
python manage.py seed_social_data
```

### 6. Start the Development Server
```powershell
python manage.py runserver
```

*(If port 8000 is occupied by another app, you can run on port 8080: `python manage.py runserver 8080`)*.

Now open your web browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo User Accounts

| Username | Password | Full Name | Bio / Role |
| :--- | :--- | :--- | :--- |
| **`alex_tech`** | `password123` | Alex Rivera | Full-Stack Engineer & Python enthusiast |
| **`sarah_design`** | `password123` | Sarah Chen | Senior Product Designer & UI/UX specialist |
| **`marcus_ai`** | `password123` | Marcus Vance | AI/ML Researcher working on agentic workflows |
| **`emma_travel`** | `password123` | Emma Watson | Photographer, explorer & storyteller |
| **`admin`** | `admin123` | CodeAlpha Admin | Superuser access to `/admin/` |

> *Tip: The Login page includes one-click autofill buttons for `@alex_tech` and `@sarah_design`!*

---

## 🧪 Running Automated Tests

Run the full automated test suite:

```powershell
python manage.py test
```

Expected output:
```
Ran 10 tests in ...s
OK
```

---

## 📁 Directory Architecture

```
social_media_platform/
├── manage.py
├── social_project/            # Project Settings & Root Routing
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                  # User Profile, Follow/Unfollow, Auth App
│   ├── models.py              # Profile, Follow models
│   ├── views.py               # Register, Login, Logout, Profile, Follow toggle, Follower lists
│   ├── urls.py
│   ├── forms.py               # RegisterForm, ProfileUpdateForm
│   ├── context_processors.py  # Suggestions & Trending topics
│   ├── admin.py
│   └── tests.py
├── posts/                     # Posts, Comments, Likes, Feed App
│   ├── models.py              # Post, Like, Comment models
│   ├── views.py               # Feed, Explore, Post CRUD, Like toggle API, Comment API
│   ├── urls.py
│   ├── forms.py               # PostForm, CommentForm
│   ├── admin.py
│   ├── tests.py
│   └── management/commands/
│       └── seed_social_data.py # Automated mock seeder
├── templates/                 # Modern UI Templates
│   ├── base.html              # 3-column layout, sidebar navigation, widgets
│   ├── posts/
│   │   ├── feed.html          # Following Feed, Explore, Post Composer
│   │   ├── post_detail.html   # Single post thread & live comments
│   │   ├── post_edit.html     # Author post editor
│   │   └── post_confirm_delete.html
│   └── accounts/
│       ├── profile.html       # Profile header, tabs (Posts, Likes), Follow button
│       ├── profile_edit.html  # Bio, location, avatar editor
│       ├── followers_list.html# Followers & Following list view
│       ├── login.html         # Login with quick autofill
│       └── register.html      # Registration form
├── static/
│   ├── css/custom.css         # Animations, forms, scrollbars
│   └── js/social.js           # AJAX like/unlike, follow/unfollow, live comments
└── README.md
```

---

## 📄 License
Created for demonstration and educational purposes as part of the CodeAlpha Internship Program.
