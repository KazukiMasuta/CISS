from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView

from . forms import TopicModelForm, TopicForm, TopicCreateForm, CommentModelForm
from .models import Topic2, Category, Comment, Vote

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def top(request):
    ctx = {'title': 'サークル'}
    return render(request, 'club/top.html', ctx)

#unused
class TopView(TemplateView,LoginRequiredMixin):
    template_name = 'club/top.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'サークルのページ'
        return ctx

#unused
class TopicListView(ListView,LoginRequiredMixin):
    template_name = 'club/top.html'
    queryset = Topic2.objects.order_by('-created')
    context_object_name = 'topic_list'

class ClubTopicView(FormView,LoginRequiredMixin):
    template_name = 'club/top.html'
    model = Topic2
    form_class = TopicCreateForm
    success_url = reverse_lazy('club:top')


    comment = Comment.objects.count()
    print(comment)

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'club/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'club/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('club:top'))

    def Comments(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comtCount = comment.objects.annotate(replies=Count('no'))


    def get_context_data(self):
        ctx = super().get_context_data()
        print('完了3-1')
        print('完了3-2')
        #ctx['posts'] = Data.objects.filter(data_id=self.kwargs['pk']).order_by('no')
        #ctx['posts'] = Topic.objects.filter(data = self.kwargs['pk']).order_by('-created')
        ctx['posts'] = Topic2.objects.annotate(vote_count=Count('vote')).order_by('-created')
        print('完了3-3')
        return ctx


"""
    def form_valid(self, form):
        form.instance.author = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'topics/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'topics/create_other_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':

            form.save_with_data(self.kwargs.get('pk'))
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('cissapp:index'))
"""


class TopicDetailView(DetailView,LoginRequiredMixin):
    template_name = 'club/detail_topic.html'
    model = Topic2
    context_object_name = 'topic'

class TopicFormView(FormView,LoginRequiredMixin):
    template_name = 'club/create_topic.html'
    form_class = TopicCreateForm
    success_url = reverse_lazy('club:top')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        form.save()
        return super().form_valid(form)

#@login_required
def topic_create(request):
    template_name = 'club/create_topic.html'
    ctx = {}
    if request.method == 'GET':
        ctx['form'] = TopicCreateForm()
        return render(request, template_name, ctx)

    if request.method == 'POST':
        topic_form = TopicCreateForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()
            return redirect(reverse_lazy('club:top'))
        else:
            ctx['form'] = topic_form
            return render(request, template_name, ctx)
# unused
class TopicCreateView(CreateView,LoginRequiredMixin):
    template_name = 'club/create_topic.html'
    form_class = TopicCreateForm
    model = Topic2
    success_url = reverse_lazy('club:top')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'club/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'club/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('club:top'))

class CategoryView(ListView,LoginRequiredMixin):
    template_name = 'club/category.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Topic2.objects.filter(category__url_code = self.kwargs['url_code'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = get_object_or_404(Category, url_code=self.kwargs['url_code'])
        return ctx

class TopicAndCommentView(FormView,LoginRequiredMixin):
    template_name = 'club/detail_topic.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        # コメント保存のためsave_with_topicメソッドを呼ぶ
        form.save_with_topic(self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('club:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic2.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment.objects.filter(
                topic_id=self.kwargs['pk']).order_by('no')
        return ctx
