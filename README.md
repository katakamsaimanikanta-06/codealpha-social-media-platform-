# ⚡ Nexus — The Modern Social Media Platform

A full-stack, responsive modern Social Media web application built with **Django**, **SQLite**, **HTML5**, **Tailwind CSS**, and **Vanilla JavaScript (AJAX)**.

Designed with a sleek, creator-first social experience featuring an electric **Sky Blue & Emerald** aesthetic, **Plus Jakarta Sans** typography, an Instagram-style **Stories reel**, an interactive **Post Studio** with character countdown, and instant AJAX interactions.

---

## ✨ Key Features

- **👤 Creator Profiles & Authentication**:
  - Secure registration, sign-in, and sign-out with instant flash toasts.
  - Profile customization: Avatar upload, Cover header banner, Display name, Bio, Location, and Website.
  - Real-time Follower count, Following count, and Posts count.
  - Tabbed creator views: **Creator Posts** and **Liked Posts**.

- **📝 Post Management (Full CRUD)**:
  - **Create**: Post Studio with live character countdown (500 limit), hashtag chips, image attachment preview, and instant publish.
  - **View**: Responsive feed stream cards and dedicated single-post thread discussions (`/post/<id>/`).
  - **Edit**: Post owners can edit post text and replace attached images (`/post/<id>/edit/`).
  - **Delete**: Secure confirmation prompt and permanent post deletion (`/post/<id>/delete/`).

- **❤️ Social Interactivity (AJAX)**:
  - **Like / Unlike**: Real-time heart toggle with bounce micro-animation and live counter without page refresh.
  - **Comments**: Post comments in real-time via AJAX, view timestamped comment threads with author avatars, and allow authors to delete comments.
  - **Follow / Unfollow**: Instant follow button on profiles, suggested creator cards, and followers lists.
  - **Followers & Following Lists**: Dedicated tabs showing follower and following user cards with direct follow toggles.
  - **Share**: 1-click "Copy post link" action with instant toast confirmation.

- **📰 Smart Feeds & Discovery**:
  - **Stories / Active Creators Reel**: Horizontal scrollable creator avatars with colorful gradient rings along the top of the feed.
  - **Following Stream**: Chronological stream of posts from creators you follow + your own posts.
  - **Explore Community**: Global stream of all posts across the community to discover new creators.
  - **Search**: Live search bar filtering posts by content, hashtag, or author username.

- **🎨 Modern 3-Column Social UI**:
  - **Left Sidebar**: Nexus brand logo, Navigation links (Home, Explore, My Profile, Settings, Admin Panel, Sign Out).
  - **Center Feed**: Sticky header, Stories reel, Post Studio, Tab Switcher, and Post stream.
  - **Right Sidebar**: Search bar, "Creators to Follow" recommendations widget, and Trending Topics.
  - **Mobile**: Responsive bottom navigation bar and mobile top header.

- **🌱 Automated Seed Data**:
  - Single command `python manage.py seed_social_data` populates realistic demo creators (`@nexus.io`), avatars, posts with imagery, follow relationships, likes, and comment threads out of the box!

---

## 🛠️ Tech Stack

- **Backend**: Python 3.13+, Django 6.1+
- **Database**: SQLite3
- **Frontend**: HTML5, Tailwind CSS (via CDN), Custom CSS, Vanilla JavaScript (AJAX)
- **Typography & Icons**: Plus Jakarta Sans, Lucide Icons
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
python manage.py migrate
```

### 5. Seed Demo Creators, Posts & Relationships
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
👉 **[http://127.0.0.1:8080/](http://127.0.0.1:8080/)**

---

## 🔑 Demo User Accounts

| Username | Password | Full Name | Bio / Role |
| :--- | :--- | :--- | :--- |
| **`alex_tech`** | `password123` | Alex Rivera | Full-Stack Software Engineer |
| **`sarah_design`** | `password123` | Sarah Chen | Senior Product Designer |
| **`marcus_ai`** | `password123` | Marcus Vance | AI/ML Researcher |
| **`emma_travel`** | `password123` | Emma Watson | Photographer & Explorer |
| **`admin`** | `admin123` | Nexus Admin | Platform Administrator (`/admin/`) |

> *Tip: The Login page includes one-click autofill buttons for `@alex_tech` and `@sarah_design`!*

---

## 🧪 Running Automated Tests

Run the full automated test suite:

```powershell
python manage.py test
```

Expected output:
```
Ran 10 tests in 25.980s
OK
System check identified no issues (0 silenced).
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
│   │   ├── feed.html          # Stories reel, Post Studio, following stream
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
│   ├── css/custom.css         # Animations, story rings, forms, scrollbars
│   └── js/social.js           # AJAX like/unlike, follow/unfollow, live comments, copy link
└── README.md
```
