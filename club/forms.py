from django import forms
from django.forms import ModelForm
from . models import Topic2, Category, Comment

class TopicCreateForm(ModelForm):
    class Meta:
        model=Topic2
        fields=[
            'title',
            'category',
            'message',
        ]

class TopicModelForm(forms.ModelForm):
    class Meta:
        model=Topic2
        fields=[
            'title',
            'category',
            'message',
        ]
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'hoge'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = '選択して下さい'

class TopicForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        max_length=255,
        required=True,
    )
    category = forms.ModelChoiceField(
        label='カテゴリー',
        queryset=Category.objects.all(),
        required=True,
        empty_label='選択して下さい',
    )
    message = forms.CharField(
        label='本文',
        widget=forms.Textarea,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'message',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    def save_with_topic(self, topic_id, commit=True):
        comment = self.save(commit=False)
        comment.topic = Topic2.objects.get(id=topic_id)
        comment.no = Comment.objects.filter(topic_id=topic_id).count() + 1
        if commit:
            comment.save()
        return comment