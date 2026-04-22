from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
        "content",
        "image",
        "created_at",
        "publication",
        "show_counted",
    )
    list_filter = ("publication",)
    search_fields = ("title",)
