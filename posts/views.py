from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views import View

from .models import Post
from .forms import PostForm


User = get_user_model()


def posts_list_view(request):

    # if not request.user.is_authenticated:
    #     return redirect(reverse('login_url'))

    if request.method == 'GET':
        if request.user.is_authenticated:
            posts = request.user.posts.all()
        else:
            posts = Post.objects.all()

        context = {
            'posts': posts
        }
        return render(request, 'posts/index.html', context=context)


def post_detail_view(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_detail.html', context={'post': post})


class PostCreateView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('login_url'))
        form = PostForm()
        return render(request, 'posts/post_create.html', context={'form': form})

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post)
        return render(request, 'posts/post_create.html', context={'form': form})


class PostUpdateView(View):

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect(reverse('login_url'))
        post = get_object_or_404(Post, id=id)
        bound_form = PostForm(instance=post)
        return render(request, 'posts/post_update.html', context={'form': bound_form,
                                                                  'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect(post)
        return render(request, 'posts/post_update.html', context={'form': form, 'post': post})


class PostDeleteView(View):

    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect(reverse('login_url'))
        post = get_object_or_404(Post, id=id)
        return render(request, 'posts/post_delete.html', context={'post': post})

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return redirect(reverse('posts_list_url'))