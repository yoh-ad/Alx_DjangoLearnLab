from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.db.models import Q

from .models import Post, Comment, Tag
from .forms import UserRegistrationForm, ProfileForm, PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.save(author=self.request.user)
        messages.success(self.request, "Post created successfully.")
        return redirect('post_list')

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_user(self):
        obj = self.get_object()
        return obj.author == self.request.user

    # Django uses test_func name; keep both for clarity
    def test_func(self):
        return self.test_user()

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.save(author=self.request.user)
        messages.success(self.request, "Post updated.")
        return redirect('post_detail', pk=self.object.pk)

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

# Comments
class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added.")
        else:
            messages.error(request, "Please correct the error below.")
        return redirect('post_detail', pk=post_id)

class CommentAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        comment = self.get_object()
        return comment.author == self.request.user

class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_queryset(self):
        # ensure nested URL post_id matches the comment's post
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.post.pk})

# Registration & Profile
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect('post_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

# Tag filtering
class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_name = self.kwargs['tag_name']
        self.tag = Tag.objects.filter(name__iexact=tag_name).first()
        if not self.tag:
            return Post.objects.none()
        return Post.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag'] = self.tag
        return ctx

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['tag'] = self.tag
        return ctx

# Search
class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        q = self.request.GET.get('q') or self.request.GET.get('query') or ''
        return Post.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q)
        ).distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx
