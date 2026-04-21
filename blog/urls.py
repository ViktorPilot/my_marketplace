from django.urls import path

from blog import views
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    path("", views.BlogListView.as_view(), name="home_blog"),
    path("detail/<int:pk>/", views.BlogDetailView.as_view(), name="detail_blog"),
    path("create/", views.BlogCreateView.as_view(), name="create_blog"),
    path("<int:pk>/update/", views.BlogUpdateView.as_view(), name="update_blog"),
    path("<int:pk>/delete/", views.BlogDeleteView.as_view(), name="delete_blog"),
    ]