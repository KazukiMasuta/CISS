from django.db.models import Count, Q
from django.http import Http404
from django.views.generic import (
        CreateView, FormView, DetailView, TemplateView, ListView, FormView)
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404

from cissapp.models import Data, Topic

import csv
from django.http import HttpResponseRedirect
from io import TextIOWrapper, StringIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext

from topics.forms import TopicCreateForm

class FirstView(ListView):
    model = Topic
    template_name = 'cissapp/first.html'


def search(request):
    query = request.GET.get('q')
    if query:
        Class = Data.objects.all()
        Class = Class.filter(
            Q(day__icontains=query) |
            Q(name__icontains=query) |
            Q(period__icontains=query) |
            Q(teacher__icontains=query)
        ).distinct()
    else:
        Class = Data.objects.all()

    class_list = Class.values()
    return render(request, 'cissapp/search.html', {'Class': Class, 'class_list': class_list, 'query': query,})

class IndexView(ListView):
    model = Topic
    template_name = 'cissapp/index.html'
    queryset = Topic.objects.order_by('-created')[:10]
    context_object_name = 'topic_list'

class TopicDetailView(FormView):
    template_name = 'cissapp/detail.html'
    form_class = TopicCreateForm

    def form_valid(self, form):
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

    def get_success_url(self):
        return reverse_lazy('cissapp:detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self):
        ctx = super().get_context_data()
        print('完了3-1')
        ctx['data'] = Data.objects.get(id=self.kwargs['pk'])
        print('完了3-2')
        #ctx['posts'] = Data.objects.filter(data_id=self.kwargs['pk']).order_by('no')
        #ctx['posts'] = Topic.objects.filter(data = self.kwargs['pk']).order_by('-created')
        ctx['posts'] = Topic.objects.filter(
            data=self.kwargs['pk']).annotate(vote_count=Count('vote')).order_by('-created')
        print('完了3-3')
        return ctx

def upload(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            class_data, created = Data.objects.get_or_create(name=line[4])
            class_data.category = line[0]
            class_data.no = line[1]
            class_data.semester = line[2]
            class_data.day = line[3]
            class_data.name = line[4]
            class_data.period = line[5]
            class_data.teacher = line[6]
            class_data.credit = line[7]
            class_data.save()

        return render(request, 'cissapp/upload.html')

    else:
        return render(request, 'cissapp/upload.html')
