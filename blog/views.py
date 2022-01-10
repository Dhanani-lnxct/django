from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.http import request
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post



def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5



    def get_context_data(self):
        all_post = Post.objects.all()
        login = self.request.user.is_authenticated

        if login == True:
            user = User.objects.get(id = self.request.user.id)
            u_post = Post.objects.all().filter(author = user ).count()

            return {'posts':all_post, 'u_post': u_post, }

        else:
            name = []
            total = {}
            for i in all_post:
                name = i.author.username
                if name in total:
                    total[name] += 1
                else:
                    total[name] =1
            print('========', total)
            return {'total': total}
        


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})