from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView

from . forms import TopicModelForm, TopicForm, TopicCreateForm, CommentModelForm
from .models import Topic3, Comment3

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def top(request):
    ctx = {'title': '物々交換'}
    return render(request, 'trade/top.html', ctx)

#unused
class TopView(TemplateView,LoginRequiredMixin):
    template_name = 'trade/top.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'サークルのページ'
        return ctx

#unused
class TopicListView(ListView,LoginRequiredMixin):
    template_name = 'trade/top.html'
    queryset = Topic3.objects.order_by('-created')
    context_object_name = 'topic_list'


class TradeTopicView(CreateView,LoginRequiredMixin):
    template_name = 'trade/top.html'
    model = Topic3
    form_class = TopicCreateForm
    success_url = reverse_lazy('trade:top')



    def form_valid(self, form):
        form.instance.user_name = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'trade/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'trade/top.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('trade:top'))
    def get_context_data(self):
        ctx = super().get_context_data()
        print('完了3-1')
        print('完了3-2')
        #ctx['posts'] = Data.objects.filter(data_id=self.kwargs['pk']).order_by('no')
        #ctx['posts'] = Topic.objects.filter(data = self.kwargs['pk']).order_by('-created')
        ctx['posts'] = Topic3.objects.annotate(vote_count=Count('vote')).order_by('-created')
        print('完了3-3')
        return ctx
"""
    def Comments(self, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comtCount = comment.objects.annotate(replies=Count('no'))
"""




class TopicDetailView(DetailView,LoginRequiredMixin):
    template_name = 'trade/detail_topic.html'
    model = Topic3
    context_object_name = 'topic'

class TopicFormView(FormView,LoginRequiredMixin):
    template_name = 'trade/create_topic.html'
    form_class = TopicCreateForm
    success_url = reverse_lazy('trade:top')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        form.save()
        return super().form_valid(form)

@login_required
def topic_create(request):
    template_name = 'trade/create_topic.html'
    ctx = {}
    if request.method == 'GET':
        ctx['form'] = TopicCreateForm()
        return render(request, template_name, ctx)

    if request.method == 'POST':
        topic_form = TopicCreateForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()
            return redirect(reverse_lazy('trade:top'))
        else:
            ctx['form'] = topic_form
            return render(request, template_name, ctx)

class TopicCreateView(CreateView,LoginRequiredMixin):
    template_name = 'trade/create_topic.html'
    form_class = TopicCreateForm
    model = Topic3
    success_url = reverse_lazy('trade:top')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'trade/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'trade/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('club:top'))

class TopicAndCommentView(FormView,LoginRequiredMixin):
    template_name = 'trade/detail_topic.html'
    form_class = CommentModelForm

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        # コメント保存のためsave_with_topicメソッドを呼ぶ
        form.save_with_topic(self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('trade:topic', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['topic'] = Topic3.objects.get(id=self.kwargs['pk'])
        ctx['comment_list'] = Comment3.objects.filter(
                topic_id=self.kwargs['pk']).order_by('no')
        return ctx