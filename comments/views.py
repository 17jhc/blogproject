from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm
# Create your views here.


def post_comment(request, post_pk):
    # 获取被评论的文章，
    # get_object_or_404获取不存在时返回404页面
    post = get_object_or_404(Post, pk=post_pk)

    # 仅处理POST请求
    if request.method == 'POST':
        # 提交数据在request.POST中，用来构造CommentForm实例
        form = CommentForm(request.POST)

        # 检查格式是否正确
        if form.is_valid():
            # 利用模型生成实例但是不保存到数据库
            comment = form.save(commit=False)
            # 关联评论和文章
            comment.post = post
            # 保存
            comment.save()
            # 重定向到详情页
            return redirect(post)
        else:
            '''
            数据不合法，重新渲染详情页，并渲染表单的错误
            所以传了三个模型变量给detail.html，分别是文章、评论列表、表单
            post.comment.set.all()方法类似post.objects.all()
            可以反向查询全部评论
            '''
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    # 不是post请求，说明没有提交数据，重定向到文章详情页
    return redirect(post)
