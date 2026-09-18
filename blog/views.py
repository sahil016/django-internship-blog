from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PostForm, CommentForm
from django.contrib import messages
from .forms import UserRegistrationForm, PostForm, CommentForm, UserProfileForm
from django.shortcuts import get_object_or_404

def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail_view(request, pk):
    posts = get_object_or_404(Post, pk=pk)
    comments = posts.comments.all().order_by('-created_at')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = posts
            new_comment.save()
            return redirect('post_detail', pk=posts.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {
        'post': posts, 
        'comments': comments, 
        'comment_form': comment_form
        })

def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            if request.user.is_authenticated:
                new_post.author = request.user
            else:
                from django.contrib.auth.models import User
                new_post.author = User.objects.first() 
            new_post.save()
            messages.success(request, 'Article published successfully!')
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/profile.html', {'user_posts': user_posts})



@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
            
    return render(request, 'blog/profile_edit.html', {'form': form})

@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Ensure only the author can edit their own post
    if post.author != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('post_detail', pk=post.pk)
        
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        
    return render(request, 'blog/post_form.html', {'form': form})
