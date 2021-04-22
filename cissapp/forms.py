from django.forms import ModelForm
from .models import Topic, Data
from django import forms

class TopicCreateForm(ModelForm):
    class Meta:
        model=Topic
        fields=[
            #'no',
            #'data',
            'title',
            'content',
            #'author',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        #self.fields['author'].widget.attrs['value'] = '匿名'
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

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