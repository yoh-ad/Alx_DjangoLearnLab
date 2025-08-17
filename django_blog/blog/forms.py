from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class PostForm(forms.ModelForm):
    tags_csv = forms.CharField(
        required=False,
        help_text="Comma-separated tags (e.g., django, web, tutorial)"
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags_csv")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['tags_csv'].initial = ", ".join(t.name for t in self.instance.tags.all())

    def save(self, author=None, commit=True):
        post = super().save(commit=False)
        if author is not None:
            post.author = author
        if commit:
            post.save()
        # handle tags
        tags_csv = self.cleaned_data.get("tags_csv", "")
        names = [t.strip() for t in tags_csv.split(",") if t.strip()]
        tag_objs = []
        for name in names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)
        post.tags.set(tag_objs)
        if commit:
            post.save()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."})
        }
