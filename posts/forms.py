from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full bg-transparent border-0 focus:ring-0 text-slate-800 placeholder-slate-400 resize-none text-base outline-none',
            'rows': 3,
            'placeholder': "What's happening in your world?",
            'maxlength': '1000'
        }),
        required=True
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'id': 'post-image-input',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = Post
        fields = ['content', 'image']


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-slate-100 focus:bg-white text-sm rounded-full py-2.5 pl-4 pr-12 border border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition outline-none',
            'placeholder': 'Write your reply...',
            'maxlength': '500'
        }),
        required=True
    )

    class Meta:
        model = Comment
        fields = ['content']
