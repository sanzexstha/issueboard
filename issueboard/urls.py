from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name="BoardList"),
    path('boards/<int:pk>/', views.TopicListView.as_view(), name="TopicList"),
    path('boards/addnew/', views.BoardCreateView.as_view(), name="BoardCreate"),
    path('boards/<int:pk>/new/', views.TopicCreateView.as_view(), name="NewIssue"),
    path('boards/<int:pk>/issues/<int:issue_pk>/',
         views.TopicPostsView.as_view(), name="TopicPosts"),
   path('boards/<int:pk>/issues/<int:issue_pk>/edit/<int:post_pk>/',
         views.PostUpdateView.as_view(), name="PostUpdate"),
     path('boards/<int:pk>/issue/<int:issue_pk>/reply/',
         views.PostReplyView.as_view(), name="PostReply"),
 
 
]