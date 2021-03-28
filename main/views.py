from django.views.generic.base import View
from django.views.generic import ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



from .models import Post, Comment
from django.contrib.auth.models import User
from .forms import CommentForm, CreateUserForm, CreatePostForm


# Create your views here.
class Home(ListView):
    model = Post
    template_name = 'friendlier/home.html'
    def get_queryset(self):
        return Post.objects.order_by('-created_at')

class UserDetail(View):
    def get(self, request, id):
        page_owner = get_object_or_404(User, id=id)

        posts = Post.objects.filter(owner=page_owner).order_by('-created_at')

        ctx = {
            'posts': posts,
            'page_owner': page_owner,
        }

        return render(request, 'friendlier/user_detail.html', ctx)


class PostDetail(View):
    def get(self, request, id, comment_form=None):
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post=post)

        if not comment_form:
            comment_form = CommentForm()

        ctx = {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
        }
        return render(request, 'friendlier/post_detail.html', ctx)



class CreateComment(View, LoginRequiredMixin):
    def post(self, request, id):
        post = Post.objects.get(id=id)

        success_url = post.get_absolute_url() # reverse( 'post-detail', id=id )
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.post = post
            comment.save()
            return redirect(success_url)
        return redirect(success_url, comment_form=form)


class CreateUser(View):
    def get(self, request):
        form = CreateUserForm()
        ctx = {'form': form}
        return render(request, 'registration/signup.html', ctx) # TODO: make a nice signup.html

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user-detail', user.id)
        # else if the user messed up the form
        ctx = {'form': form}
        return render(request, 'registration/signup.html', ctx)


class CreatePost(View, LoginRequiredMixin):
    def get(self, request):
        form = CreatePostForm()
        ctx = {'form': form}
        return render(request, 'friendlier/create_post.html', ctx) # TODO: create this

    def post(self, request):
        form = CreatePostForm(request.POST, request.FILES)

        # return render(request, 'friendlier/create_post.html', {'form': form})

        if not form.is_valid():
            ctx = {
                'form' : form,
            }
            return render(request, 'friendlier/create_post.html', ctx)
        post = form.save(commit=False)
        post.owner = self.request.user
        post.save()
        print(f"The user's id is {request.user.id}")
        # next = reverse('user-detail', int(request.user.id))
        return redirect(reverse('user-detail', args=[request.user.id]))

