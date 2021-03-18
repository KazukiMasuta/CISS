from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, FormView, DetailView

from . forms import TopicModelForm, TopicForm, TopicCreateForm, CommentModelForm
from .models import Topic3, Comment3

def top(request):
    ctx = {'title': '物々交換'}
    return render(request, 'trade/top.html', ctx)

class TopView(TemplateView):
    template_name = 'trade/top.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'サークルのページ'
        return ctx
    
class TopicListView(ListView):
    template_name = 'trade/top.html'
    queryset = Topic3.objects.order_by('-created')
    context_object_name = 'topic_list'

class TopicDetailView(DetailView):
    template_name = 'trade/detail_topic.html'
    model = Topic3
    context_object_name = 'topic'

class TopicFormView(FormView):
    template_name = 'trade/create_topic.html'
    form_class = TopicCreateForm
    success_url = reverse_lazy('trade:top')

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        form.save()
        return super().form_valid(form)

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

class TopicCreateView(CreateView):
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

class TopicAndCommentView(FormView):
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
        ctx['comment_list'] = Comment.objects.filter(
                topic_id=self.kwargs['pk']).order_by('no')
        return ctx