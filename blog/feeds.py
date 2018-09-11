from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    # 聚合阅读器标题
    title = "Django 博客演示项目"
    # 通过聚合器转到的网站地址
    link = '/'
    # 显示在聚合阅读器的描述信息
    description = 'Django 博客演示项目测试文章'
    # 内容

    def items(self):
        return Post.objects.all()

    # 内容标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)
    # 内容描述
    def item_description(self, item):
        return item.body
