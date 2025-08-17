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
    # Expose existing tags for selection
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    # Allow creating new tags from comma-separated text
    new_tags = forms.CharField(
        required=False,
        help_text="Add new tags (comma-separated)"
    )

    class Meta:
        model = Post
        fields = ("title", "content", "tags", "new_tags")

    def save(self, author=None, commit=True):
        post = super().save(commit=False)
        if author is not None:
            post.author = author
        if commit:
            post.save()

        # Existing selected tags
        selected_tags = list(self.cleaned_data.get("tags", []))

        # Create any new tags
        fresh = []
        for name in [t.strip() for t in self.cleaned_data.get("new_tags", "").split(",") if t.strip()]:
            tag, _ = Tag.objects.get_or_create(name=name)
            fresh.append(tag)

        # Assign union of both sets
        post.tags.set(list({*selected_tags, *fresh}))
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
