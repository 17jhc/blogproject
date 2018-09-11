from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import markdown
from django.utils.html import strip_tags
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)
    # 文章正文
    body = models.TextField()
    # 创建时间和最后一次修改时间
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 摘要,默认必须输入数据，否则报错,更改Blank
    excerpt = models.CharField(max_length=200, blank=True)
    # 分类和标签
    # 一个文章对应一个分类,一个分类可对应多个文章
    # 一个文章可以有多个标签，一个标签可以使用多个文章
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 浏览量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.markdown(self.body, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md)[:54]
        super(Post, self).save(*args, **kwargs)