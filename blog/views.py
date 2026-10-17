"""
Django Views Module for Blog Application

This module contains view functions and classes for managing blog posts, user authentication,
and profile management. It implements best practices including query optimization, caching,
and permission-based access control.

Author: Blog Development Team
Last Updated: 2024
"""

from django.db import connection
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Count
from django.core.cache import cache

from .models import Post
from .forms import PostForm, CommentForm, UserRegistrationForm, UserProfileForm


# =====================================================================
# POST LIST VIEWS
# =====================================================================

def post_list_view(request):
    posts = (Post.objects
             .select_related('author')
             .prefetch_related('comments')
             .annotate(comment_count=Count('comments'))
             .order_by('-created_at'))
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail_view(request, pk):
    """
    Display the details of a specific blog post.
    
    Note: This view currently has a bug - it renders the post_list template instead
    of a post_detail template. The function should be fixed to render individual
    post details with full comments and discussion.
    
    Args:
        request (HttpRequest): The HTTP request object
        pk (int): Primary key of the post to display
        
    Returns:
        HttpResponse: Rendered template with post details
        
    TODO: Fix template name to 'blog/post_detail.html' and modify view logic
    """
    posts = Post.objects.select_related('author').prefetch_related('comments').annotate(
        comment_count=Count('comments')
    ).order_by('-created_at')
    
    return render(request, 'blog/post_list.html', {'posts': posts})


# =====================================================================
# POST CREATION AND EDITING VIEWS
# =====================================================================

def post_create_view(request):
    """
    Handle creation of new blog posts.
    
    Supports both GET (display form) and POST (process form) requests.
    Automatically assigns the current authenticated user as the post author.
    Falls back to the first user if the request is anonymous (not recommended for production).
    
    Workflow:
        1. GET request: Display empty PostForm
        2. POST request: Validate form, save post with current user as author
        3. Success: Redirect to post list with success message
        
    Security Note:
        The fallback to User.objects.first() for unauthenticated users is a security
        risk and should be restricted with @login_required decorator in production.
    
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered form template or redirect to post_list on success
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Save form data without committing to database
            new_post = form.save(commit=False)
            
            # Assign author based on authentication status
            if request.user.is_authenticated:
                new_post.author = request.user
            else:
                # SECURITY WARNING: This fallback is unsafe for production
                # Consider adding @login_required decorator instead
                from django.contrib.auth.models import User
                new_post.author = User.objects.first()
            
            # Commit the post to the database
            new_post.save()
            messages.success(request, 'Article published successfully!')
            return redirect('post_list')
    else:
        # Initialize an empty form for GET requests
        form = PostForm()
    
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def post_edit_view(request, pk):
    """
    Handle editing of existing blog posts.
    
    Only the post author can edit their own posts. Attempts by other users are
    rejected with an error message and redirect.
    
    Workflow:
        1. GET request: Display pre-filled form with current post data
        2. POST request: Validate changes and update the post
        3. Success: Redirect to post detail with success message
        4. Permission Denied: Redirect to post_list with error message
    
    Args:
        request (HttpRequest): The HTTP request object
        pk (int): Primary key of the post to edit
        
    Returns:
        HttpResponse: Rendered form template or redirect based on result
        
    Raises:
        Http404: If the post with the given pk does not exist
    """
    # Retrieve the post or raise 404 if not found
    post = get_object_or_404(Post, pk=pk)
    
    # Verify that only the author can edit the post
    if post.author != request.user:
        messages.error(request, "You do not have permission to edit this post.")
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        # Bind form to POST data and post instance for update
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            # Save the updated post
            form.save()
            messages.success(request, 'Article updated successfully!')
            return redirect('post_detail', pk=post.pk)
    else:
        # Initialize form with current post data
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form})


# =====================================================================
# AUTHENTICATION AND REGISTRATION VIEWS
# =====================================================================

def register_view(request):
    """
    Handle user account registration.
    
    Provides a registration form for new users to create accounts.
    Password validation and user model constraints are handled by UserRegistrationForm.
    
    Workflow:
        1. GET request: Display empty registration form
        2. POST request: Validate form and create new user
        3. Success: Redirect to login page with success message
        
    Args:
        request (HttpRequest): The HTTP request object
        
    Returns:
        HttpResponse: Rendered registration template or redirect to login on success
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        # Initialize an empty form for GET requests
        form = UserRegistrationForm()
    
    return render(request, 'blog/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Custom login view that extends Django's built-in LoginView.
    
    Provides a personalized welcome message upon successful authentication.
    Uses a custom template for the login form.
    
    Attributes:
        template_name (str): Path to the login template
        
    Methods:
        form_valid(form): Called when login form is valid; displays welcome message
    """
    template_name = 'blog/login.html'
    
    def form_valid(self, form):
        """
        Handle successful login by displaying a personalized welcome message.
        
        Args:
            form: The validated login form containing user credentials
            
        Returns:
            HttpResponse: Result of parent's form_valid method (typically redirect)
        """
        # Display personalized welcome message
        messages.success(self.request, f"Welcome back, {form.get_user().username}!")
        return super().form_valid(form)


# =====================================================================
# USER PROFILE VIEWS
# =====================================================================

@login_required
def profile_view(request):
    """
    Display the authenticated user's profile page with their posts.
    
    Implements caching for post count to reduce database queries. The cache
    is invalidated after 5 minutes to balance performance with data freshness.
    
    Caching Strategy:
        - Cache Key: f'user_{request.user.id}_post_count'
        - TTL: 300 seconds (5 minutes)
        - Fallback: Database query if cache miss
    
    Args:
        request (HttpRequest): The HTTP request object (must be authenticated)
        
    Returns:
        HttpResponse: Rendered profile template with user's posts and post count
        
    Note:
        This view requires authentication. Unauthenticated users are redirected
        to the login page by the @login_required decorator.
    """
    # Generate a unique cache key for this user's post count
    cache_key = f'user_{request.user.id}_post_count'
    
    # Attempt to retrieve post count from cache
    post_count = cache.get(cache_key)
    
    # If cache miss, query database and cache the result for 5 minutes (300 seconds)
    if post_count is None:
        post_count = Post.objects.filter(author=request.user).count()
        cache.set(cache_key, post_count, 300)

    # Fetch all user's posts ordered by most recent first
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    return render(request, 'blog/profile.html', {
        'user_posts': user_posts,
        'post_count': post_count
    })


@login_required
def profile_edit_view(request):
    """
    Handle editing of the authenticated user's profile information.
    
    Allows users to update their profile details such as username, email,
    and other profile-related information defined in UserProfileForm.
    
    Workflow:
        1. GET request: Display pre-filled form with current user data
        2. POST request: Validate changes and update user profile
        3. Success: Redirect to profile view with success message
    
    Args:
        request (HttpRequest): The HTTP request object (must be authenticated)
        
    Returns:
        HttpResponse: Rendered profile edit template or redirect to profile on success
        
    Note:
        This view requires authentication. Unauthenticated users are redirected
        to the login page by the @login_required decorator.
    """
    if request.method == 'POST':
        # Bind form to POST data and current user instance
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # Save the updated profile information
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        # Initialize form with current user data
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'blog/profile_edit.html', {'form': form})