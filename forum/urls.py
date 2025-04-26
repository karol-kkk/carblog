from django.urls import path
from . import views # from current folder import the neighbour file views for views methods usage

urlpatterns = [
    path('', views.post_home, name='post_home'),
    path('frequent_questions', views.frequent_questions),
    path('create', views.post_create, name='post_create'),
    path('<int:pk>', views.PostDetailView.as_view(), name='post_show'),
    path('<int:pk>/update', views.update_post, name='post_update'),
    path('<int:pk>/delete', views.PostDeleteView.as_view(), name='post_delete'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment')
]
 