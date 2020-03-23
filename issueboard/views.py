
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, FormView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import TopicCreateForm, PostCreateForm, BoardCreateForm
from .models import Board, Issue, Post


class BoardListView(ListView):
    template_name = "boards/board_list.html"
    model = Board
   


class TopicListView(ListView):
    template_name = "boards/topic_list.html"
    paginate_by = 8

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




class TopicCreateView(FormView):
    form_class = TopicCreateForm
    template_name = "boards/new_topic.html"

    def form_valid(self, form):
        topic = form.cleaned_data.get('topic')
        message = form.cleaned_data.get('message')
        board = get_object_or_404(Board, pk=self.kwargs['pk'])
        new_topic = Issue.objects.create(
            subject=topic, board=board, starter=self.request.user)
        new_post = Post.objects.create(
            message=message, topic=new_topic, created_by=self.request.user)

        return redirect('TopicList', self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = get_object_or_404(Board, pk=self.kwargs['pk'])
        return context


class TopicPostsView(DetailView):
    model = Issue
    template_name = "boards/topic_posts.html"

    def get_object(self):
        self.topic = get_object_or_404(
            Issue, board__pk=self.kwargs['pk'], pk=self.kwargs['topic_pk'])
        
        return self.topic

 

class PostUpdateView(UpdateView):
    model = Post
    fields = ['message']
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'
    template_name = "boards/update_post.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('TopicPosts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

class PostReplyView(CreateView):
    template_name = "boards/reply_issue.html"
    form_class = PostCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topic'] = get_object_or_404(Issue, pk=self.kwargs['topic_pk'])
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.topic = get_object_or_404(
            Issue, pk=self.kwargs['topic_pk'])
        instance.created_by = self.request.user
        return super().form_valid(form)
 