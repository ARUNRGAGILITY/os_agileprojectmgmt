model = """

from django.db import models

class Category(models.Model):
    name = models.CharField(max.max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



"""

admin_py = """
from django.contrib import admin
from .models import Category, Post

admin.site.register(Category)
admin.site.register(Post)

"""

forms_py = """

from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']

"""
add_post_list_view_search = """
def post_list(request):
    query = request.GET.get('query', '')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

"""

views_post_py = """

from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post, Category

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


"""

urls_py = """
from django.urls import path
from .views import post_list, post_detail, post_create, post_update, post_delete

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_update, name='post_update'),
   <path('post/<int:pk>/delete/', post_delete, name='post_delete'),
]


"""

post_list_html = """

<!DOCTYPE html>
<html>
<head>
    <title>Blog</是>
</head>
<body>
    <h1>Blog Posts</h1>
    {% for post in posts %}
    <div>
        <h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
        <p>{{ post.body|slice:":200" }}...</p>
    </div>
    {% endfor %}
</body>
</html>

"""

add_post_list_search_html = """

<form method="get">
    <input type="text" name="query" placeholder="Search posts...">
    <button type="submit">Search</button>
</form>

"""

post_edit_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Edit Post</title>
</head>
<body>
    <h1>{% if form.instance.pk %}Edit{% else %}Create{% endif %} Post</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'post_list' %}">Back to post list</a>
</body>
</html>

"""

post_detail_html = """

<!DOCTYPE html>
<html>
<head>
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>
    <p>Category: {{ post.category }}</p>
    <a href="{% url 'post_update' pk=post.pk %}">Edit</a>
    <form action="{{ url 'post_delete' pk=post.pk }}" method="post" style="display:inline;">
        {% csrf_token %}
        <button type="submit">Delete</button>
    </form>
    <a href="{% url 'post_list' %}">Back to posts</a>
</body>
</html>


"""

# category CRUD

view_categories_py = """
from .models import Category
from django.forms import ModelForm

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_edit.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/category_edit.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('category_list')

"""

category_list_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Categories</title>
</head>
<body>
    <h1>Categories</h1>
    {% for category in categories %}
    <div>
        <h2>{{ category.name }}</h2>
        <a href="{% url 'category_update' pk=category.pk %}">Edit</a>
        <form action="{% url 'category_delete' pk=category.pk %}" method="post" style="display:inline;">
            {% csrf_token %}
            <button type="submit">Delete</button>
        </form>
    </div>
    {% endfor %}
    <a href="{% url 'category_create' %}">Add New Category</a>
</body>
</html>

"""

category_edit_html = """
<!DOCTYPE html>
<html>
<head>
    <title>{% if form.instance.pk %}Edit{% else %}Create{% endif %} Category</title>
</head>
<body>
    <h1>{% if form.instance.pk %}Edit{% else %}Create{% endif %} Category</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'category_list' %}">Back to categories</a>
</body>
</html>

"""

category_urls_py = """

path('categories/', category_list, name='category_list'),
path('category/new/', category_create, name='category_create'),
path('category/<int:pk>/edit/', category_update, name='category_update'),
path('category/<int:pk>/delete/', category_delete, name='category_delete'),

"""

post_pagination = """
<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
</head>
<body>
    <h1>Blog Posts</h1>
    <form method="get">
        <input type="text" name="query" placeholder="Search posts..." value="{{ request.GET.query }}">
        <button type="submit">Search</button>
    </form>
    {% for post in page_obj %}
    <div>
        <h2><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h2>
        <p>{{ post.body|slice:":200" }}...</p>
    </div>
    {% endfor %}
    <div>
        <span class="step-links">
            {% if page_obj.has_previous %}
                <a href="?page=1&query={{ request.GET.query }}">first</a>
                <a href="?page={{ page_obj.previous_page_number }}&query={{ request.GET.query }}">previous</a>
            {% endif %}
            <span class="current">
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.
            </span>
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}&query={{ request.GET.query }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}&query={{ request.GET.query }}">last</a>
            {% endif %}
        </span>
    </div>
</body>
</html>

"""

post_views_py = """
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def post_list(request):
    query = request.GET.get('query', '')
    posts = Post.objects.all()
    if query:
        posts = posts.filter(title__icontains=query)

    # Pagination setup
    paginator = Paginator(posts, 5)  # Display 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_two_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

"""

# recursive category

tag = """

from django import template
from ..models import Category

register = template.Library()

@register.simple_tag
def recursive_category_display(category):
    return _recursive_render(category)

def _recursive_render(category, level=0):
    subcategories = category.subcategories.all()
    if subsettings:
        content = "<ul>"
        for subcategory in subcategories:
            content += f"<li>{'--' * level} {subcategory.name}</li>"
            content += _recursive_render(subcategory, level+1)
        content += "</ul>"
        return content
    else:
        return f"<li>{'--' * level} {category.name}</li>"

"""

sample_display = """
{% load category_tags %}

<ul>
    {% for category in root_categories %}
        {{ recursive_category_display category }}
    {% endfor %}
</ul>

"""

sample_view = """
from django.shortcuts import render
from .models import Category

def some_view(request):
    root_categories = Category.objects.filter(parent=None)
    return render(request, 'your_template.html', {'root_categories': root_classes})

"""

blog_landing_view = """
from django.shortcuts import render
from .models import Post, Category
from django.core.paginator import Paginator

def blog_landing(request):
    query = request.GET.get('query', '')
    posts = Post.objects.all().order_by('-created_at')
    if query:
        posts = posts.filter(title__icontains=query)

    # For categories display
    categories = Category.objects.filter(parent=None)

    # Pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/blog_landing.html', {
        'page_obj': page_obj,
        'categories': categories
    })

"""

template_blog_landing = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blog Landing Page</title>
</head>
<body>
    <header>
        <h1>Blog</h1>
        <form action="" method="get">
            <input type="text" name="query" placeholder="Search blog posts..." value="{{ request.GET.query }}">
            <button type="submit">Search</button>
        </form>
    </header>
    <aside>
        <h2>Categories</h2>
        <ul>
            {% for category in categories %}
                <li><a href="{% url 'category_posts' category.id %}">{{ category.name }}</a></li>
            {% endfor %}
        </ul>
    </aside>
    <main>
        <h2>Recent Posts</h2>
        {% for post in page_obj %}
            <div>
                <h3><a href="{% url 'post_detail' post.id %}">{{ post.title }}</a></h3>
                <p>{{ post.body|slice:":200" }}...</p>
            </div>
        {% endfor %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page={{ page_obj.previous_page_number }}&query={{ request.GET.query }}">Previous</a>
            {% endif %}
            <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.</span>
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}&query={{ request.GET.query }}">Next</a>
            {% endif %}
        </div>
    </main>
</body>
</html>

"""

url_blog_landing = """
from django.urls import path
from .views import blog_landing

urlpatterns = [
    path('', blog_landing, name='blog_landing'),
]

"""

# category posts

view_category_posts = """
def category_posts(request, category_id):
    category = Category.objects.get(id=category_id)
    posts = category.posts.all().order_by('-created_at')
    return render(request, 'blog/category_posts.html', {'posts': posts, 'category': category})

"""

category_posts_url = """
path('category/<int:category_id>/', category_posts, name='category_posts'),

"""

## breadcrumbs

model_bread_crumbs = """

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_breadcrumbs(self):
        breadcrumbs = []
        current = self
        while current is not None:
            breadcrumbs.append(current)
            current = current.parent
        return breadcrumbs[::-1]  # Reverse the list to start from the root

"""

category_posts = """
def category_posts(request, category_id):
    category = Category.objects.get(id=category_id)
    posts = category.posts.all().order_by('-created_at')
    breadcrumbs = category.get_breadcrumbs()
    return render(request, 'blog/category_posts.html', {
        'posts': posts,
        'category': category,
        'breadcrumbs': breadcrumbs
    })

"""

breadcrumb_in_template = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ category.name }}</title>
</head>
<body>
    <header>
        <nav>
            <ul>
                {% for crumb in breadcrumbs %}
                    <li>
                        <a href="{% url 'category_posts' crumb.id %}">{{ crumb.name }}</a>
                        {% if not forloop.last %} &gt; {% endif %}
                    </li>
                {% endfor %}
            </ul>
        </nav>
    </header>
    <main>
        <h1>{{ category.name }}</h1>
        {% for post in posts %}
            <article>
                <h2><a href="{% url 'post_detail' post.id %}">{{ post.title }}</a></h2>
                <p>{{ post.body|slice:":200" }}...</p>
            </article>
        {% endfor %}
    </main>
</body>
</html>

"""

post_model_with_slug = """
# model
from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    body = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Only set the slug when the object is created initially
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
        
    # handle collisions
    def save(self, *args, **kwargs):
    if not self.id:
        self.slug = slugify(self.title)
        # Ensure the slug is unique
        original_slug = self.slug
        num = 1
        while Post.objects.filter(slug=self.slug).exists():
            self.slug = f'{original_slug}-{num}'
            num += 1
    super(Post, self).save(*args, **kwargs)


# detail
from django.shortcuts import get_object_or_484, render

def post_detail(request, slug):
    post = get_object_or_484(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post})

# url
from django.urls import path
from .views import post_detail, post_list, post_create, post_update, post_delete

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('post/<slug:slug>/edit/', post_update, name='post_update'),
    path('post/<slug:slug>/delete/', post_delete, name='post_delete'),
]

# template
{% for post in posts %}
<div>
    <h2><a href="{% url 'post_detail' slug=post.slug %}">{{ post.title }}</a></h2>
    <p>{{ post.body|slice:":200" }}...</p>
</div>
{% endfor %}


"""

## likes, appreciate

likes_appreciates = """

# model 
from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    body = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)
    appreciates = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='appreciated_posts', blank=True)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_appreciates(self):
        return self.appreciates.count()


# views
from django.shortcuts import get_object_or_404, redirect
from .models import Post

def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    return redirect('post_detail', slug=slug)

def appreciate_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        if request.user in post.appreciates.all():
            post.appreciates.remove(request.user)
        else:
            post.appreciates.add(request.user)
    return redirect('post_detail', slug=slug)


# urls
from django.urls import path
from .views import like_post, appreciate_post

urlpatterns = [
    path('post/<slug:slug>/like/', like_post, name='like_post'),
    path('post/<widget:slug>/appreciate/', appreciate_post, name='eyeweary_post'),
]


# template
<form action="{% url 'like_post' slug=post.slug %}" method="post">
    {% csrf_token %}
    <button type="submit">Like</button>
    ({{ post.total_likes() }})
</form>

<form actions="{% verification 'limit_of_posts' flag=suggestion.MARVELOUS %}" subject="getting">
    {% get_companies "Overwatch%}
    <bind type="add">Add</cross>
    ({{ graphics.general_startups() }})
</any>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ post.title }}</title>
</head>
<body>
    <h1>{{ post.title }}</h1>
    <p>{{ post.body }}</p>

    <!-- Like button form -->
    <form action="{% url 'like_post' slug=post.slug %}" method="post">
        {% csrf_token %}
        <button type="submit">Like</button>
        ({{ post.total_likes() }})
    </form>

    <!-- Appreciate button form -->
    <form action="{% url 'appreciate_post' slug=post.slug %}" method="post">
        {% csrf_token %}
        <button type="submit">Appreciate</button>
        ({{ post.total_appreciates() }})
    </form>

    <!-- Link to read more or details -->
    <a href="{% url 'post_detail' slug=post.slug %}">Read More</a>
</body>
</html>

# form code
<!-- Corrected "Like" button form -->
<form action="{% url 'like_post' slug=post.slug %}" method="post">
    {% csrf_token %}
    <button type="submit">Like</button>
    ({{ post.total_likes() }})
</form>

<!-- Assumed "Appreciate" button form, corrected and simplified -->
<form action="{% url 'appreciate_post' slug=post.slug %}" method="post">
    {% csrf_token %}
    <button type="submit">Appreciate</button>
    ({{ post.total_appreciates() }})
</form>

# order by likes and appreciation
from django.shortcuts import render
from django.db.models import Count
from .models import Post

def post_list(request):
    query = request.GET.get('query', '')
    posts = Post.objects.annotate(
        total_likes=Count('likes'),
        total_appreciates=Count('appreciates')
    ).order_by('-total_likes', '-total_appreciates')

    if query:
        posts = posts.filter(title__icontains=query)

    return render(request, 'blog/post_list.html', {'posts': posts})


"""