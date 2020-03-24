
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView, DeleteView
from .forms import IssueCreateForm, PostCreateForm, BoardCreateForm
from .models import Board, Issue, Post
 


class BoardListView(ListView):
    template_name = "boards/board_list.html"
    model = Board

# class ReplyDelView(DeleteView):     
#     model = Post
#     template_name = "boards/reply_confirm_delete.html"
#     success_url = reverse_lazy('IssuePost')
 

class IssueListView(ListView):
    template_name = "boards/issue_list.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["board"] = get_object_or_404(Board,pk=self.kwargs['pk'])
        return context

    def get_queryset(self):
        queryset = Issue.objects.filter(board__id=self.kwargs['pk'])
        return queryset

class BoardCreateView(FormView):
    form_class = BoardCreateForm
    template_name = "boards/new_board.html"

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        description = form.cleaned_data.get('description')
        new_board = Board.objects.create(
            name=name, description=description)
        return redirect('BoardList')




class IssueCreateView(FormView):
    form_class = IssueCreateForm
    template_name = "boards/new_issue.html"

    def form_valid(self, form):
        issue = form.cleaned_data.get('issue')
        message = form.cleaned_data.get('message')
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        new_topic = Issue.objects.create(
            subject=issue, board=board, starter=self.request.user)
        new_post = Post.objects.create(
            message=message, issue=new_topic, created_by=self.request.user)
        return redirect('IssueList', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = get_object_or_404(Board, pk=self.kwargs['pk'])
        return context


class IssuePostsView(DetailView):
    model = Issue
    template_name = "boards/issue_posts.html"

    def get_object(self):
        self.issue = get_object_or_404(
            Issue, board__pk=self.kwargs['pk'], pk=self.kwargs['issue_pk'])
        return self.issue

class PostDelView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    template_name = "boards/reply_confirm_delete.html"


    def get_success_url(self, **kwargs):
        
        return reverse_lazy('IssuePosts', kwargs={'pk': self.kwargs['pk'], 'issue_pk': self.kwargs['issue_pk']})

class IssueDelView(DeleteView):
    model = Issue
    pk_url_kwarg = 'issue_pk'
    context_object_name = 'issue'
    template_name = "boards/reply_confirm_delete.html"


    def get_success_url(self, **kwargs):     
        return reverse_lazy('IssueList', kwargs={'pk': self.kwargs['pk']})

class PostUpdateView(UpdateView):
    model = Post
    fields = ['message']
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    template_name = "boards/update_posts.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('IssuePosts', pk=post.issue.board.pk, issue_pk=post.issue.pk)

class PostReplyView(CreateView):
    template_name = "boards/reply_issue.html"
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['issue'] = get_object_or_404(Issue, pk=self.kwargs['issue_pk'])
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.issue = get_object_or_404(
            Issue, pk=self.kwargs['issue_pk'])
        instance.created_by = self.request.user
        return super().form_valid(form)


    def get_success_url(self, **kwargs):
        return reverse_lazy('IssuePosts', kwargs={'pk': self.kwargs['pk'], 'issue_pk': self.kwargs['issue_pk']})