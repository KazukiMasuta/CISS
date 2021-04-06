from django.db import models
from accounts.models import User

class TopicManager(models.Manager):
    # Topic操作に関する処理を追加
    pass

class CommentManager(models.Manager):
    # Comment操作に関する処理を追加
    pass

class Topic3(models.Model):
    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        'タイトル',
        max_length=255,
        null = False,
        blank = False,
    )
    message = models.TextField(
        verbose_name='本文',
        null=True,
        blank=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    modified = models.DateTimeField(
        auto_now=True,
    )
    pub_flg = models.BooleanField(
        default=True,
    )
    objects = TopicManager()

    def __str__(self):
        return self.title

class Comment3(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )
    no = models.IntegerField(
        default=0,
    )
    user_name = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    topic = models.ForeignKey(
        Topic3,
        on_delete=models.PROTECT,
    )
    message = models.TextField(
        verbose_name='投稿内容'
    )
    pub_flg = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    objects = CommentManager()

    def __str__(self):
        return '{}-{}'.format(self.topic.id, self.no)

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
        Topic3,
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