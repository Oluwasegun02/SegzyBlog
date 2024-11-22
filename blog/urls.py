from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_post, name='create_post'),
    path('my-posts/', views.user_posts,name='user_posts'),  # Add URL for user-specific posts
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),  # Add URL for category filtering
    path('tag/<int:tag_id>/', views.posts_by_tag, name='posts_by_tag'),
    path('post/<int:post_id>/<slug:slug>/', views.post_detail, name='post_detail'),
    path('search/', views.search_results, name='search_results'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),

]
