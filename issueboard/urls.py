from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name="BoardList"),
    path('boards/<int:pk>/', views.IssueListView.as_view(), name="IssueList"),
    path('boards/addnew/', views.BoardCreateView.as_view(), name="BoardCreate"),
    path('boards/<int:pk>/new/', views.IssueCreateView.as_view(), name="NewIssue"),
    path('boards/<int:pk>/issues/<int:issue_pk>/',
         views.IssuePostsView.as_view(), name="IssuePosts"),
   path('boards/<int:pk>/issues/<int:issue_pk>/edit/<int:post_pk>/',
         views.PostUpdateView.as_view(), name="PostUpdate"),
    path('boards/<int:pk>/issues/<int:issue_pk>/reply/',
         views.PostReplyView.as_view(), name="PostReply"),
    path('boards/<int:pk>/issues/<int:issue_pk>/delete',
         views.IssueDelView.as_view(), name="IssueDel"),
    path('boards/<int:pk>/issues/<int:issue_pk>/delete/<int:post_pk>/',
         views.PostDelView.as_view(), name="PostReplyDel"),
]