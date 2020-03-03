from datetime import datetime
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone


from .models import Blog
from .forms import BlogForm


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog/list.html', {'blogs': blogs})


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'blog/detail.html', {'context': blog, "active": 'blogs'})


def blog_new(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.edited = timezone.now()
            form.save()
            return redirect('blog:blog_list')
    else:
        form = BlogForm()
    return render(request, 'blog/new.html', {"form": form, "active": "new"})


def blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.edited = timezone.now()
            blog.save()
            return redirect('blog:blog_detail', pk=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'blog/edit.html', {'form': form})


def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    blog.delete()
    messages.success(request, f'Deleted pk={pk}')
    return redirect('blog:blog_list')
