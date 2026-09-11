from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Post
from .forms import PostForm, CommentForm

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
                new_post.author = User.objects.get(username='Anonymous')
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})