from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class Data(models.Model):
    category = models.CharField("科目種別", blank=True, max_length=100)
    no = models.CharField("授業番号", blank=True, max_length=10)
    semester = models.CharField("学期", blank=True, max_length=5)
    day = models.CharField("曜日", blank=True, max_length=1)
    name = models.CharField("科目", blank=True, max_length=20)
    period = models.CharField("時限", blank=True, max_length=2)
    teacher = models.CharField("担当教員", blank=True, max_length=30)
    credit = models.CharField("単位", blank=True, max_length=1)

    class Meta:
        verbose_name = '授業'
        verbose_name_plural = '授業一覧'

    def __str__(self):
        return(self.name)


# Create your models here.
class TopicManager(models.Manager):
    # Topic操作に関する処理を追加
    pass

class CommentManager(models.Manager):
    # Comment操作に関する処理を追加
    pass

class CategoryManager(models.Manager):
    # Category操作に関する処理を追加
    pass

class Topic(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )
    no = models.IntegerField(
        default=0,
    )
    data = models.ForeignKey(
        Data,
        on_delete=models.PROTECT,
    )

    title = models.CharField(
        'タイトル',
        max_length=30,
        null=True,
        blank=False,
    )
    content = models.TextField(
        verbose_name='本文',
        null=True,
        blank=False,
    )
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True
    )
    time = models.DateTimeField(
        default=timezone.now
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        auto_now=True,
    )
    objects = TopicManager()

    class Meta:
        verbose_name = '投稿'
        verbose_name_plural = '投稿一覧'


    def __str__(self):
        return '{}-{}'.format(self.data.id, self.no)

class VoteManager(models.Manager):
    def create_vote(self, ip_address, comment_id):
        vote = self.model(
            ip_address=ip_address,
            comment_id = comment_id
        )
        try:
            vote.save()
        except:
            return False
        return True

class Vote(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        null=True,
    )
    ip_address = models.CharField(
        'IPアドレス',
        max_length=50,
    )

    objects = VoteManager()

    def __str__(self):
        return '{}-{}'.format(self.topic.title, self.topic.no)