from .models import BlogPost, Category, Comment, Tag, Like
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogPostForm, CommentForm
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.contrib import messages
import smtplib
from email.mime.text import MIMEText
from jinja2 import Template
import os
from dotenv import load_dotenv
load_dotenv()
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


# Create your views here.

def index(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()

    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/index.html', {'page_obj': page_obj, 'categories': categories, 'tags': tags})

def about_page(request):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    return render(request, 'blog/about.html',  {'categories': categories, 'tags': tags})


def contact_page(request):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        message = request.POST.get('message', "")
        if name and email and message:
            # Prepare email content
            subject = f"New Contact Us Message from {name}"
            context = {
                'subject': subject,
                'body': f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            }
            
            # Load the template
            template_path = os.path.join(os.path.dirname(__file__), 'template.html')
            with open(template_path, 'r') as f:
                template = Template(f.read())
            html_message = template.render(context)
            
            # Create MIMEText object
            msg = MIMEText(html_message, 'html')
            msg['Subject'] = subject
            msg['From'] = email
            msg['To'] = 'adebayoogunniyi8@gmail.com'
            
            # Send email
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # Use App Password
                    server.sendmail(email, 'adebayoogunniyi8@gmail.com', msg.as_string())
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                print(e)  # For debugging
                messages.error(request, 'There was an error sending your message. Please try again later.')
        else:
            messages.error(request, 'Please fill out all fields.')
        return redirect('contact_page') 
    return render(request, 'blog/contact.html', {'categories': categories, 'tags': tags})

def privacy_policy(request):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    return render(request, 'blog/privacy_policy.html', {'categories': categories, 'tags': tags})

@login_required
def create_post(request):
    categories = Category.objects.all() 
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Assign the currently logged-in user as the author
            post.save()
            return redirect('user_posts')  # Redirect to the home page after saving
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form, 'categories': categories, 'tags': tags})

@login_required
def user_posts(request):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/user_posts.html', {'posts': posts, 'categories': categories, 'tags': tags})

def posts_by_category(request, category_id):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    category = get_object_or_404(Category, id=category_id)
    posts = BlogPost.objects.filter(category=category).order_by('-created_at')
    return render(request, 'blog/posts_by_category.html', {'category': category, 'posts': posts, 'categories': categories, 'tags': tags})

def post_detail(request, post_id, slug):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    post = get_object_or_404(BlogPost, id=post_id, slug=slug)
    comments = post.comments.all()
    user_liked = False

    # Check if the user has already liked the post
    if request.user.is_authenticated:
        user_liked = post.likes.filter(user=request.user).exists()

    # Initialize the comment form
    comment_form = CommentForm()

    if request.method == 'POST':
        # Handle 'like' functionality
        if 'like' in request.POST:
            if request.user.is_authenticated:
                if not user_liked:
                    Like.objects.create(post=post, user=request.user)  # Add like
                else:
                    post.likes.filter(user=request.user).delete()  # Remove like
            return redirect('post_detail', post_id=post.id, slug=post.slug)

        # Handle comment submission
        if 'comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect('post_detail', post_id=post.id, slug=post.slug)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'like_count': post.likes.count(),
        'categories': categories, 
        'tags': tags,
    })

def posts_by_tag(request, tag_id):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    tag = get_object_or_404(Tag, id=tag_id)
    posts = BlogPost.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts, 'categories': categories, 'tags': tags})

def search_results(request):
    categories = Category.objects.all()  # Retrieve all categories
    tags = Tag.objects.all()
    query = request.GET.get('q')
    results = BlogPost.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    return render(request, 'blog/search_results.html', {'results': results, 'query': query, 'categories': categories, 'tags': tags})