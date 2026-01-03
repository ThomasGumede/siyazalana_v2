from django.contrib.auth.decorators import login_required
from siyazalana_home.forms import CommentForm, PostForm
from siyazalana_home.models import Blog, BlogCategory
from siyazalana_home.utilities.decorators import user_not_superuser_or_staff
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage

@csrf_exempt
def tinymce_image_upload(request):
    if request.method == "POST":
        if 'file' in request.FILES:
            image = request.FILES['file']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(image.name, image)
            file_url = settings.MEDIA_URL + filename
            return JsonResponse({'location': file_url})
    return JsonResponse({'error': 'No image uploaded'}, status=400)

def blogs(request, category_slug=None):
    query = request.GET.get("query", None)
    template = "blogs/blogs.html"
    model = Blog
    
    if category_slug:
        category = get_object_or_404(BlogCategory, slug=category_slug)
        blogs = model.objects.filter(category=category)
        if query:
            blogs = blogs.filter(title__icontains=query)
    else:
        blogs = model.objects.all()
        if query:
            blogs = blogs.filter(title__icontains=query)

    context = {"posts": blogs, "query": query}

    return render(request, template, context)

@login_required
@user_not_superuser_or_staff
def all_blogs(request):
    query = request.GET.get("query", None)
    blogs = Blog.objects.filter(author = request.user)
    if query:
        blogs = blogs.filter(title__icontains=query)
    return render(request, 'dashboard/blogs/blogs.html', {"blogs": blogs})


def blog_details(request, post_slug):
    
    blog = get_object_or_404(Blog.objects.select_related("category").prefetch_related("comments"), slug=post_slug)
    recent_posts = Blog.objects.order_by("-created")[:5]

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.user.is_authenticated:
                instance.commenter = request.user
            else:
                instance.commenter = None
            instance.post = blog
            instance.save()
            messages.success(request, "Comment added successfully")
            return redirect('siyazalana_home:details-blog', post_slug=blog.slug)
        else:
            messages.error(request, "Comment not added, fix errors below")
            return redirect('siyazalana_home:details-blog', post_slug=blog.slug)
        
    form = CommentForm()
    return render(request, 'blogs/blog-details.html', {"post": blog, "recent_posts": recent_posts, "form": form})

@login_required
@user_not_superuser_or_staff
def create_blog(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            post = form.save(commit=False)
            post.author = request.user
            post.description = form.cleaned_data.get("content", None)[:100]
            post.save()
            messages.success(request, "Blog post was created successfully!")
            return redirect("siyazalana_home:all-blogs")
        else:
            messages.error(request, "Something went wrong trying to create your blog post")
            return render(request, "dashboard/blogs/create-blog.html", {"form": form})
        
    return render(request, "dashboard/blogs/create-blog.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def update_blog(request, post_slug):
    blog = get_object_or_404(Blog.objects.select_related("category").prefetch_related("comments"), slug=post_slug)
    if blog.author != request.user:
        messages.error(request, "Sorry, you cannot update blog post that are not yours")
        return redirect("dashboard:all-blogs")
    
    form = PostForm(instance=blog)
    if request.method == "POST":
        form = PostForm(instance=blog, data=request.POST, files=request.FILES)
        if form.is_valid() and form.is_multipart():
            post = form.save()
            return redirect("siyazalana_home:all-blogs")
        else:
            messages.error(request, "Something went wrong trying to update your blog post")
            return render(request, "dashboard/blogs/update-blog.html", {"form": form})

    return render(request, "dashboard/blogs/update-blog.html", {"form": form})

@login_required
@user_not_superuser_or_staff
def delete_blog(request, post_slug):
    blog = get_object_or_404(Blog.objects.filter(author = request.user).select_related("category").prefetch_related("comments"), slug=post_slug)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog was deleted successfully")
        return redirect("home:all-blogs")
    
    return render(request, "dashboard/blogs/delete-blog.html", {"blog": blog})