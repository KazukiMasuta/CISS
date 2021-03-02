
"""
from django import forms
class ClassSearchForm(forms.Form):
    no = forms.CharField(label='授業番号', max_length=10)
    day = forms.CharField(label='曜日',max_length=1)
    name = forms.CharField(label='科目',max_length=20)
    period = forms.CharField(label='時限',max_length=2)
    teacher = forms.CharField(label='担当教員',max_length=30)
"""

from django.forms import ModelForm
from cissapp.models import Topic, Data
from django import forms

class TopicCreateForm(ModelForm):
    class Meta:
        model=Topic
        fields=[
            #'no',
            #'data',
            'title',
            'content',
            'author',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['value'] = '匿名'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        return kwargs

    def save_with_data(self, data_id, commit=True):
        topic = self.save(commit=False)
        topic.data = Data.objects.get(id=data_id)
        #なんでここ .topic なの？ -> dataにしたら治った
        topic.no = Topic.objects.filter(data_id=data_id).count() + 1
        print('以下デバック-----------')
        print(data_id)
        print(type(topic))
        print(topic.no)
        print('---------------------')
        # どうも　cissapp_datapost.data_id となってるのがおかしいっぽい
        if commit:
            topic.save()
        return topic


class noclassTopicCreateForm(ModelForm):
    class Meta:
        model=Topic
        fields=[
            #'no',
            #'data',
            'title',
            'content',
            'author',
        ]

    def __init__(self, *args, **kwargs):
        # kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['value'] = '匿名'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super().get_form_kwargs()
        return kwargs

    def save_with_data(self, data_id, commit=True):
        topic = self.save(commit=False)
        topic.data = Data.objects.get(id=data_id)
        #なんでここ .topic なの？ -> dataにしたら治った
        topic.no = Topic.objects.filter(data_id=data_id).count() + 1
        print('以下デバック-----------')
        print(data_id)
        print(type(topic))
        print(topic.no)
        print('---------------------')
        # どうも　cissapp_datapost.data_id となってるのがおかしいっぽい
        if commit:
            topic.save()
        return topic

"""
#form内の詳細設定
class TopicForm(forms.Form):
    subject = forms.CharField(
        label='科目名',
        max_length=255,
        required=True,
    )
    author = forms.CharField(
        label='お名前',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'value': '匿名'}),
    )

    context = forms.CharField(
        label='本文',
        widget=forms.Textarea,
        required=True,
    )
"""