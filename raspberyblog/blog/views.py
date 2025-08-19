from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm, SignUpForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(approved=True)

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user  # Optional if you store who wrote the comment
                comment.save()
                return HttpResponseRedirect(reverse('post_detail', args=[post.id]))
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Toggle like: if user already liked, remove; otherwise, add
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

    return HttpResponseRedirect(reverse('post_detail', args=[post_id]))

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
