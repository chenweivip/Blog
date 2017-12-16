from django.db import models

from django.contrib.auth.models import AbstractUser

import django.utils.timezone as timezone
# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):
    '''用户信息'''
    nid = models.BigAutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    email = models.EmailField(verbose_name='邮箱')
    tel = models.CharField(verbose_name='手机号码', max_length=11, unique=True, null=True, blank=True)
    avatar = models.FileField(verbose_name='头像', upload_to='avatar/', default="/avatar/default.png")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)



    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '用户详情表'


class Blog(models.Model):
    '''站点信息表'''
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    user = models.OneToOneField(to='UserInfo', to_field='nid')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '站点信息表'


class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '博客个人分类表'
        ordering = ['title']


class Article(models.Model):
    '''文章表'''

    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='创建时间',default = timezone.now)
    update_time = models.DateTimeField(verbose_name='最后修改时间', auto_now=True)

    read_count = models.IntegerField(verbose_name='阅读数', default=0)
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    up_count = models.IntegerField(verbose_name='点赞数', default=0)
    down_count = models.IntegerField(verbose_name='被踩数', default=0)
    '''查询多于编辑，避免跨表查询'''
    category = models.ForeignKey(verbose_name='文章类型', to='Category', to_field='nid', blank=True, null=True)
    user = models.ForeignKey(verbose_name='所属用户', to='UserInfo', to_field='nid')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag', 
        through_fields=('article', 'tag'),
    )
    siteCategory=models.ForeignKey(to='SiteCategory',verbose_name='所属博客系统分类',related_name='article',null=True,blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '文章表'

class SiteMenu(models.Model):
    '''博客主页左侧菜单'''
    title=models.CharField(verbose_name='分类主标题', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '博客主页主菜单标题'

class SiteCategory(models.Model):
    '''博客主页左侧子菜单'''
    title = models.CharField(verbose_name='分类子标题', max_length=32)
    siteMenu=models.ForeignKey(verbose_name='所属主标题',to='SiteMenu')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '博客主页子菜单标题'


class ArticleDetail(models.Model):
    '''文章内容表'''
    nid = models.BigAutoField(primary_key=True)
    content = models.TextField(verbose_name='文章内容')

    article = models.OneToOneField(verbose_name='所属文章', to='Article', to_field='nid')

    class Meta:
        verbose_name_plural = '文章内容表'


class Comment(models.Model):
    '''评论表'''
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='评论时间', auto_now_add=True)
    up_count = models.IntegerField(verbose_name='评论点赞数', default=0)
    user = models.ForeignKey(verbose_name='评论人', to='UserInfo', to_field='nid')
    article = models.ForeignKey(verbose_name='评论的文章', to='Article', to_field='nid', related_name='article_comment')
    parent_comment = models.ForeignKey(verbose_name='父级评论', to='Comment', blank=True, null=True, default=None,
                                       related_name='comment_mutual')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '评论表'


class CommentUp(models.Model):
    '''点赞表'''
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='点赞人', to='UserInfo', null=True)
    comment = models.ForeignKey(verbose_name='评论的点赞', to='Comment', null=True)

    class Meta:
        verbose_name_plural = '评论点赞表'


class ArticleUp(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='点赞人', to='UserInfo', null=True)
    article = models.ForeignKey(verbose_name='点赞的文章', to='Article', null=True)
    class Meta:
        verbose_name_plural = '文章点赞表'
        unique_together = [
            ('user', 'article'),
        ]


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '标签博客表'


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')



    class Meta:
        verbose_name_plural = '文章标签表'
        unique_together = [
            ('article', 'tag'),
        ]
