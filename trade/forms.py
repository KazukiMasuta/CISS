from django import forms
from django.forms import ModelForm
from . models import Topic3, Comment3

class TopicCreateForm(ModelForm):
    class Meta:
        model=Topic3
        fields=[
            'title',
            'message',
        ]

        widgets = {
            'message': forms.Textarea(
                    attrs={
                        'rows':4, 'cols':7,
                        'placeholder': '本文だお'
                        }
                    )
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
#unused
class TopicModelForm(forms.ModelForm):
    class Meta:
        model=Topic3
        fields=[
            'title',
            'message',
        ]
        widgets = {
            'title' : forms.TextInput(attrs={'class': 'hoge'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TopicForm(forms.Form):
    title = forms.CharField(
        label='タイトル',
        max_length=255,
        required=True,
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
        model = Comment3
        fields = [
            'message',
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    def save_with_topic(self, topic_id, commit=True):
        comment = self.save(commit=False)
        comment.topic = Topic3.objects.get(id=topic_id)
        comment.no = Comment3.objects.filter(topic_id=topic_id).count() + 1
        if commit:
            comment.save()
        return comment