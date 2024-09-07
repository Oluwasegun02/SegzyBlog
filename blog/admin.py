from django.contrib import admin
from .models import BlogPost, Category, Tag
from ckeditor.widgets import CKEditorWidget
from django import forms

# Register your models here.
try:
    admin.site.unregister(BlogPost)
except admin.sites.NotRegistered:
    pass
class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Enable CKEditor in admin form

    class Meta:
        model = BlogPost
        fields = '__all__'

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title
    search_fields = ('title', 'author__username', 'content')

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Category)
admin.site.register(Tag)