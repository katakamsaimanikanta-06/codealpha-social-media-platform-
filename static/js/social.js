/**
 * CodeAlpha Social Media Platform - JavaScript Interactions
 * Handles AJAX likes, follow/unfollow, live comments, image previews, and toasts.
 */

// CSRF Token Helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie('csrftoken') || (document.querySelector('[name=csrfmiddlewaretoken]') ? document.querySelector('[name=csrfmiddlewaretoken]').value : '');

// Toast Notification System
function showToast(message, type = 'info') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none px-4';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  const bgClass = type === 'error' ? 'bg-rose-600' : (type === 'success' ? 'bg-emerald-600' : 'bg-slate-900');
  
  toast.className = `toast-enter flex items-center justify-between p-3.5 text-white rounded-xl shadow-xl pointer-events-auto text-xs font-medium ${bgClass}`;
  toast.innerHTML = `
    <span>${message}</span>
    <button class="ml-3 text-white/75 hover:text-white" onclick="this.parentElement.remove()">✕</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('toast-enter');
    toast.classList.add('toast-exit');
    setTimeout(() => toast.remove(), 250);
  }, 3500);
}

document.addEventListener('DOMContentLoaded', () => {
  
  // 1. Like / Unlike AJAX Handling
  document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const postId = button.dataset.postId;
      const url = `/post/${postId}/like/`;
      const icon = button.querySelector('.like-icon');
      const countSpan = button.querySelector('.like-count');

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
          }
        });

        if (response.status === 401 || response.status === 403 || response.redirected) {
          window.location.href = '/accounts/login/';
          return;
        }

        const data = await response.json();
        if (data.status === 'success') {
          countSpan.textContent = data.likes_count;
          if (data.liked) {
            icon.classList.remove('text-slate-400');
            icon.classList.add('text-rose-500', 'fill-rose-500', 'heart-pop');
            button.classList.add('text-rose-500');
            button.classList.remove('text-slate-500');
            setTimeout(() => icon.classList.remove('heart-pop'), 300);
          } else {
            icon.classList.remove('text-rose-500', 'fill-rose-500');
            icon.classList.add('text-slate-400');
            button.classList.remove('text-rose-500');
            button.classList.add('text-slate-500');
          }
        }
      } catch (err) {
        console.error('Like toggle failed', err);
      }
    });
  });

  // 2. Follow / Unfollow AJAX Handling
  document.querySelectorAll('.follow-toggle-btn').forEach(button => {
    button.addEventListener('click', async (e) => {
      e.preventDefault();
      const username = button.dataset.username;
      const url = `/accounts/user/${username}/follow/`;

      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
          }
        });

        if (response.status === 401 || response.status === 403 || response.redirected) {
          window.location.href = '/accounts/login/';
          return;
        }

        const data = await response.json();
        if (data.status === 'success') {
          showToast(data.message, 'success');
          
          if (data.following) {
            button.textContent = 'Following';
            button.classList.remove('bg-slate-900', 'text-white', 'hover:bg-indigo-600');
            button.classList.add('bg-slate-100', 'text-slate-700', 'border', 'border-slate-300', 'hover:bg-rose-50', 'hover:text-rose-600', 'hover:border-rose-200');
          } else {
            button.textContent = 'Follow';
            button.classList.add('bg-slate-900', 'text-white', 'hover:bg-indigo-600');
            button.classList.remove('bg-slate-100', 'text-slate-700', 'border', 'border-slate-300', 'hover:bg-rose-50', 'hover:text-rose-600', 'hover:border-rose-200');
          }

          // Update followers count badge on profile page if present
          const followersCountEl = document.getElementById('profile-followers-count');
          if (followersCountEl && button.dataset.isProfileTarget === "true") {
            followersCountEl.textContent = data.followers_count;
          }
        } else {
          showToast(data.message || 'Action failed', 'error');
        }
      } catch (err) {
        console.error('Follow toggle error', err);
      }
    });
  });

  // 3. Image preview in Post Composer
  const imageInput = document.getElementById('post-image-input');
  const previewContainer = document.getElementById('image-preview-container');
  const previewImg = document.getElementById('image-preview');
  const removeImgBtn = document.getElementById('remove-image-btn');

  if (imageInput && previewContainer && previewImg) {
    imageInput.addEventListener('change', () => {
      const file = imageInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          previewImg.src = e.target.result;
          previewContainer.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
      }
    });

    if (removeImgBtn) {
      removeImgBtn.addEventListener('click', () => {
        imageInput.value = '';
        previewImg.src = '';
        previewContainer.classList.add('hidden');
      });
    }
  }

  // 4. AJAX Comment Submission (on post detail page)
  const commentForm = document.getElementById('ajax-comment-form');
  if (commentForm) {
    commentForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const input = commentForm.querySelector('input[name="content"]');
      const content = input.value.trim();
      if (!content) return;

      const formData = new FormData(commentForm);
      const url = commentForm.action;

      try {
        const response = await fetch(url, {
          method: 'POST',
          body: formData,
          headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
          }
        });

        if (response.status === 401 || response.redirected) {
          window.location.href = '/accounts/login/';
          return;
        }

        const data = await response.json();
        if (data.status === 'success') {
          input.value = '';
          showToast('Comment posted!', 'success');

          // Append to comments list
          const commentsList = document.getElementById('comments-list');
          const noCommentsNotice = document.getElementById('no-comments-notice');
          if (noCommentsNotice) noCommentsNotice.remove();

          const commentEl = document.createElement('div');
          commentEl.className = 'flex gap-3 py-3 border-b border-slate-100 last:border-0';
          
          const avatarMarkup = data.author_avatar 
            ? `<img src="${data.author_avatar}" alt="${data.author_name}" class="w-8 h-8 rounded-full object-cover shrink-0">`
            : `<div class="w-8 h-8 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-xs shrink-0">${data.author_name.charAt(0).toUpperCase()}</div>`;

          commentEl.innerHTML = `
            ${avatarMarkup}
            <div class="flex-grow space-y-1">
              <div class="flex items-center gap-2">
                <a href="/accounts/user/${data.author_username}/" class="font-bold text-xs text-slate-900 hover:text-indigo-600">
                  ${data.author_name}
                </a>
                <span class="text-[11px] text-slate-400">@${data.author_username} · Just now</span>
              </div>
              <p class="text-xs text-slate-700 leading-relaxed">${data.content}</p>
            </div>
          `;

          if (commentsList) {
            commentsList.prepend(commentEl);
          }

          // Update comments count badge
          const countBadge = document.getElementById('comments-count-badge');
          if (countBadge) countBadge.textContent = data.comments_count;
        }
      } catch (err) {
        console.error('Comment submission failed', err);
        commentForm.submit();
      }
    });
  }

  // 5. Auto dismiss flash alerts
  document.querySelectorAll('.server-alert').forEach(alert => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });
});
