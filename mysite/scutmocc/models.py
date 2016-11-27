# coding: utf-8
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Nickname = models.CharField(max_length=10)
    College = models.CharField(max_length=20)
    # College = models.ForeignKey(College),修改验证
    Sex = models.NullBooleanField(null=True)
    Signature = models.CharField(max_length=100, null=True)
    Fb_sum = models.IntegerField(default=0)
    Hf_sum = models.IntegerField(default=0)
    Gz_sum = models.IntegerField(default=0)
    Bgz_sum = models.IntegerField(default=0)
    Sc_sum = models.IntegerField(default=0)
    Rank = models.IntegerField(default=0)

    def __str__(self):
        return self.user.last_name


def update_person(sender, instance, created, **kwargs):
    if created:
        person = Person()
        person.user = instance
        person.save()
    else:
        instance.person.save()


models.signals.post_save.connect(update_person, sender=User)


class Activity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Act_intro = models.CharField(max_length=200)
    Act_image = models.ImageField(upload_to='photos/%Y/%m/%d')

    def __str__(self):
        return self.user.last_name


def update_activity(sender, instance, created, **kwargs):
    if created:
        activity = Activity()
        activity.user = instance
        activity.save()

    else:
        instance.activity.save()


models.signals.post_save.connect(update_activity, sender=User)


# Lesson repo
class LabelField(models.Model):
    Lesson = {
        ('a', '项目'),
        ('b', '理论课'),
        ('c', '技能')
    }
    Label_Kind = models.CharField(max_length=1, choices=Lesson)
    Label_Name = models.CharField(max_length=50)

    def __str__(self):
        return self.Label_Name


# Submit Lesson
class SubmitLes(models.Model):
    Person_Id = models.ForeignKey(User)
    Label_Id = models.ForeignKey(LabelField)
    Les_Name = models.CharField(max_length=60)
    Les_Plan = models.CharField(max_length=200)
    Les_Time = models.IntegerField()
    Les_Way = models.CharField(max_length=200, null=True)
    Les_Price = models.IntegerField()
    Les_Merge = models.IntegerField()  # 0～3 社团 0~10
    Les_Another = models.CharField(max_length=150, null=True)
    Les_Term = models.IntegerField(default=1)
    Les_Next = models.DateField(null=True)
    Les_Status = models.BooleanField()

    def __str__(self):
        return self.Les_Name


# Comment Lesson
class CommentField(models.Model):
    Les_Id = models.ForeignKey(SubmitLes)
    Person_Id = models.ForeignKey(User)
    Comment = models.CharField(max_length=500)

    def __str__(self):
        return self.Comment


# Answer Lesson
class AnswerField(models.Model):
    Comment_Id = models.ForeignKey(CommentField)
    Person_Id = models.ForeignKey(User)
    Answer = models.CharField(max_length=500)

    def __str__(self):
        return self.Answer


# Relation of Choice Lesson
class ChoiceLes(models.Model):
    Les_Id = models.ForeignKey(SubmitLes)
    Person = models.ForeignKey(User)
    Ch_Date = models.DateField()
    End = models.BooleanField()
    Les_Assess = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.id


#   Board
class Board(models.Model):
    Field = [
        ('a', '活动区'),
        ('b', '问题区'),
        ('c', '话题区')
    ]
    Board_name = models.CharField(max_length=1, choices=Field, default='a')
    Gg_content = models.CharField(max_length=200)
    Jrzt_sum = models.IntegerField(default=0)
    Zrzt_sum = models.IntegerField(default=0)
    Zt_sum = models.IntegerField(default=0)

    def __str__(self):
        for x in self.Field:
            if self.Board_name == x[0]:
                return x[1]


# College
class College(models.Model):
    College_Name = models.CharField(max_length=30)
    College_Account = models.IntegerField()

    def __str__(self):
        return self.College_Name


#  Theme ,考虑去掉统计信息
class Theme(models.Model):
    Content = models.TextField()
    Title = models.CharField(max_length=50)
    Fb_date = models.DateTimeField(auto_now_add=True)
    Zjhf_date = models.DateTimeField(auto_now_add=True)
    Hf_sum = models.IntegerField(default=0)
    Zjhfr = models.ForeignKey(User, related_name='hfr_set')
    Zd = models.BooleanField()
    Dz_sum = models.IntegerField(default=0)
    Board_type = models.ForeignKey(Board)
    Fbr = models.ForeignKey(User, related_name='fbr_set')
    Yd_sum = models.IntegerField(default=0)
    Legal = models.BooleanField(default=True)
    Sc_sum = models.IntegerField(default=0)
    College_type = models.ForeignKey(College)

    def __str__(self):
        return self.Title


# BBS answer, 不区分回复主题和评论回复
class ThemeAnswer(models.Model):
    Hfr_Id = models.ForeignKey(User)
    # Lc_no = models.IntegerField()
    Fb_date = models.DateTimeField(auto_now_add=True)
    Theme_Id = models.ForeignKey(Theme, null=True)
    raw_content = models.CharField(max_length=500)
    display_content = models.CharField(max_length=500)
    Dz_sum = models.IntegerField(default=0)
    Legal = models.BooleanField(default=True)
    # ThemeAnswer_Id = models.ForeignKey("self", null=True)

    def __str__(self):
        return self.Hf_Content


# Collect Theme
class CollectTheme(models.Model):
    Yh_Id = models.ForeignKey(User)
    Theme_Id = models.ForeignKey(Theme)
    Is_Collected = models.BooleanField(default=False)

    def __str__(self):
        return self.Theme_Id


# Pay attention
class Attention(models.Model):
    Fs_Id = models.ForeignKey(User, related_name='fen')
    Ox_Id = models.ForeignKey(User, related_name='Ou')
    Is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.Fs_Id


# 点赞主题或者回复
class Dianzan(models.Model):
    Fbr_Id = models.ForeignKey(User)
    Theme_Id = models.ForeignKey(Theme, null=True)
    ThemeAnswer_Id = models.ForeignKey(ThemeAnswer, null=True)
    Is_Dianzan = models.BooleanField(default=False)


