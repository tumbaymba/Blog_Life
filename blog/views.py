import random
from datetime import date
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, TemplateView
from blog.forms import BlogForm
from blog.models import Blog
from users.models import User


class BlogCreateView(CreateView):
    """Создание публикации"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.author = self.request.user
            self.object.date_of_creation = date.today()
            self.object.save()

        return super().form_valid(form)


class BlogListView(ListView):
    """Получение листа публикаций без подписки"""
    model = Blog
    extra_context = {
        'title': " Блог без подписки",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True, is_subscribed=False)
        return queryset


class BlogSubscriptionListView(ListView):
    """Получение листа публикаций по подписке"""
    model = Blog
    template_name = 'blog/blog_list_subscription.html'
    extra_context = {
        'title': " Блог по подписке",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True, is_subscribed=True)
        return queryset


class BlogAuthorListView(ListView):
    """Получение листа публикаций за автором"""
    model = Blog
    template_name = 'blog/blog_list_author.html'
    extra_context = {
        'title': " Блог Пользователя как автора ",
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user:
            queryset = queryset.filter(author=self.request.user.pk)
        return queryset


class BlogDetailView(DetailView):
    """Публикация полностью"""
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    """Редактирование публикацию"""
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    """Удаление публикации"""
    model = Blog
    success_url = reverse_lazy('blog:list')


def toogle_activity(request, pk):
    """Снять или опубликовать статью"""
    blog_item = get_object_or_404(Blog, pk=pk)
    if blog_item.is_published:
        blog_item.is_published = False
    else:
        blog_item.is_published = True
    blog_item.save()
    return redirect('blog:list')


class IndexView(TemplateView):
    """Главная"""
    template_name = 'blog/index.html'
    extra_context = {
        'title': 'Главная',
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['publish_blog_count'] = len(Blog.objects.filter(is_published=True))
        context_data['users_count'] = len(User.objects.all())
        context_data['object_list'] = random.sample(list(Blog.objects.filter(is_subscribed=False, is_published=True)), 3)

        return context_data


def contacts(request):
    """Контакты"""
    context = {
        'title': "Контакты",
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name} ({phone}, {email}): {message}")

    return render(request, 'blog/contacts.html', context)
