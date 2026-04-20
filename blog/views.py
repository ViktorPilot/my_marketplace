from django.views.generic import ListView

from django.shortcuts import render

from blog.models import Blog


class BlogListView(ListView):
    model = Blog
