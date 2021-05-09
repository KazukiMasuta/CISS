
from django.db.models import Count, Q
from django.http import Http404
from django.views.generic import (
        CreateView, FormView, DetailView, TemplateView, ListView, FormView)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from io import TextIOWrapper, StringIO
from django.contrib.auth.mixins import LoginRequiredMixin

from cissapp.models import Data, Topic
import csv
from .forms import TopicCreateForm, noclassTopicCreateForm
from django.template import RequestContext

class TopicsTop(TemplateView):
    template_name = 'topics/topics_top.html'
    model = Topic

"""
class TopicDetailView(DetailView):
    template_name = 'topics/detail_topic.html'
    model = Topic
    context_object_name = 'topic'

def topic_create(request):
    template_name = 'topics/create_topic.html'

    ctx = {}
    if request.method == 'GET':
        ctx['form'] = TopicCreateForm()
        return render(request, template_name, ctx)

    if request.method == 'POST':
        topic_form = TopicCreateForm(request.POST)
        if topic_form.is_valid():
            topic_form.save()

            return redirect(reverse_lazy('cissapp:index'))
        else:
            ctx['form'] = topic_form
            return render(request, template_name, ctx)
"""


class CreateTopicTop(TemplateView):
    template_name = 'topics/create_topic.html'
    model = Topic

class TopicFormView(FormView):
    template_name = 'topics/create_class_topic.html'
    form_class = TopicCreateForm
    model = Topic
    success_url = reverse_lazy('cissapp:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'topics/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'topics/create_class_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            form.save()
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('cissapp:index'))

class TopicDetailView(CreateView,LoginRequiredMixin):
    template_name = 'topics/detail.html'
    form_class = TopicCreateForm
    model = Topic
    success_url = reverse_lazy('cisapp:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'topics/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'topics/detail.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            form.save_with_data(self.kwargs.get('pk'))
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('topics:detail'))

    def get_success_url(self):
        return reverse_lazy('topics:detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        print('完了3-1')
        ctx['data'] = Data.objects.get(id=self.kwargs['pk'])

        #ctx['posts'] = Data.objects.filter(data_id=self.kwargs['pk']).order_by('no')
        #ctx['posts'] = Topic.objects.filter(data = self.kwargs['pk']).order_by('-created')
        ctx['posts'] = Topic.objects.filter(
            data=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('-created')

        print('完了3-3')
        return ctx


class noclassTopicFormView(FormView):
    template_name = 'topics/create_other_topic.html'
    form_class = noclassTopicCreateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            return render(self.request, 'topics/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'topics/create_other_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':

            form.save_with_data(data_id = 5020)
            return super().form_valid(form)
        else:
            return redirect(reverse_lazy('cissapp:index'))

    def get_success_url(self):
        return reverse_lazy('cissapp:detail', kwargs={'pk': 5020})
"""
class TopicCreateView(CreateView,LoginRequiredMixin):
    template_name = 'topics/create_topic.html'
    form_class = TopicCreateForm
    model = Topic
    success_url = reverse_lazy('topics:detail')


    def form_valid(self, form):
        form.instance.user_name = self.request.user
        ctx = {'form': form}
        if self.request.POST.get('next', '') == 'confirm':
            ctx['data'] = Data.objects.get(id=self.kwargs['pk'])
            return render(self.request, 'topics/confirm_topic.html', ctx)
        if self.request.POST.get('next', '') == 'back':
            return render(self.request, 'topics/create_topic.html', ctx)
        if self.request.POST.get('next', '') == 'create':
            form.save_with_data(self.kwargs.get('pk'))
            return super().form_valid(form)
        else:
            # 正常動作ではここは通らない。エラーページへの遷移でも良い
            return redirect(reverse_lazy('topics:detail'))

    def get_success_url(self):
        return reverse_lazy('topics:detail', kwargs={'pk': self.kwargs['pk']})
"""
class SubjectView(ListView):
    template_name = 'topics/subject.html'
    context_object_name = 'topic_list'

    def get_queryset(self):
        return Data.objects.filter(name = self.kwargs['name'])

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['name'] = get_object_or_404(Data, name=self.kwargs['name'])
        return ctx