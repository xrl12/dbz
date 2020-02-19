from django.db import models
from django.contrib.auth.models import AbstractUser
from DjangoUeditor.models import UEditorField
# Create your models here.

# 父类
class Father(models.Model):
    is_show = models.BooleanField(verbose_name='是否删除',default=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间',auto_now=True)
    class Meta():
        abstract = True


# 用户表
class BlosUser(AbstractUser):
    phone = models.CharField(verbose_name='手机号',max_length=11)

    def __str__(self):
        return self.phone

# 轮播图
class Banner(Father):
    image = models.ImageField(verbose_name='图片',upload_to='banner/%Y/%m/%d')
    link = models.URLField(verbose_name='跳转地址')
    position = models.IntegerField(verbose_name='排序',default=0)
    title = models.CharField(verbose_name='标题',max_length=10)
    def __str__(self):
        return self.title
    class Meta():
        ordering = ['position']
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

# 分类
class Category(Father):
    name = models.CharField(verbose_name='分类名字',max_length=12)
    position = models.IntegerField(verbose_name='排序',default=0)
    def __str__(self):
        return self.name
    class Meta():
        ordering = ['position']
        verbose_name = '分类'
        verbose_name_plural = verbose_name

# 标签
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名',max_length=10)
    position = models.IntegerField(verbose_name='排序',default=0)
    def __str__(self):
        return self.name
    class Meta():
        ordering = ['position']
        verbose_name = '标签'
        verbose_name_plural = verbose_name

# 文章类
class Article(Father):
    title = models.CharField(verbose_name='文章名字',max_length=10)
    vnum = models.IntegerField(verbose_name='浏览量')
    cover = models.ImageField(verbose_name='文章封面',upload_to='artImg/%Y/%d/%d')
    content = UEditorField(width=600,height=300,toolbars='full',
                           imagePath='content/%(basename)s_%(datetime)s.%(extname)s'
                           ,filePath='files/')
    intro = models.CharField(verbose_name='文章简介',max_length=255)
    position = models.IntegerField(verbose_name='排序',default=0)
    is_top = models.BooleanField(verbose_name='是否置顶',default=False)

    blosuser = models.ForeignKey(to=BlosUser,on_delete=models.CASCADE)
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)

    tag = models.ManyToManyField(to=Tag)

    def __str__(self):
        return self.title
    class Meta():
        ordering = ['-create_time']
        verbose_name = '文章'
        verbose_name_plural = verbose_name

# 友情链接
class FriendLink(Father):
    link = models.URLField(verbose_name='友情链接')
    name = models.CharField(verbose_name='友情链接',max_length=10)
    def __str__(self):
        return self.name
    class Meta():
        ordering = ['create_time']
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

# 导航表
class Nav(Father):
    name = models.CharField(verbose_name='导航表',max_length=10)
    position = models.IntegerField(verbose_name='配序',default=0)
    link = models.CharField(verbose_name='跳转地址',max_length=20)
    def __str__(self):
        return self.name
    class Meta():
        ordering = ['position']
        verbose_name = '导航表'
        verbose_name_plural = verbose_name

# 广告表
class Ad(Father):
    name = models.CharField(verbose_name='广告名字',max_length=100)
    img = models.ImageField(verbose_name='广告图片')
    position = models.IntegerField(verbose_name='配序',default=0)
    link = models.URLField(verbose_name='跳转地址')
    def __str__(self):
        return self.name
    class Meta():
        ordering = ['position']
        verbose_name = '广告表'
        verbose_name_plural = verbose_name


# 评论表
class Comment(Father):
    title = models.CharField(verbose_name='评论',max_length=100)
    position = models.IntegerField(verbose_name='排序',default=0)
    users = models.ForeignKey(to=BlosUser,on_delete=models.CASCADE)
    article = models.ForeignKey(to=Article,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    class Meta():
        ordering = ['-create_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name
