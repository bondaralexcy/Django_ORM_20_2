from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from pytils.translit import slugify
from blog.models import Blog
from blog.forms import BlogForm, BlogManagerForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = "blog/blog_list.html"
    context_object_name = (
        "object_list"  # Это было не обязательно. По умолчанию и так object_list
    )
    extra_context = {"title": "Разговоры"}  # Передача статических данных
    login_url = "catalog:home"

    def get_queryset(self, *args, **kwargs):
        """Выводим только опублткованные статьи"""
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(is_published=True)


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    template_name = "blog/blog_detail.html"
    extra_context = {"title": "Детализация"}

    def get_object(self, queryset=None):
        """Метод get_object() получает данные из вызова метода get_object() родителя
        и возвращает измененный объект
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Счетчик просмотров
        self.object.save()
        return self.object


class BlogCreateView(LoginRequiredMixin, CreateView):
    """При создании нового блога динамически формировать slug name для заголовка"""

    model = Blog
    fields = ["title", "content", "image", "is_published"]
    success_url = reverse_lazy("blog:blog_list")
    extra_context = {"title": "Создать"}

    def form_valid(self, form):
        blog = form.save()
        user = self.request.user
        blog.owner = user
        blog.slug = slugify(blog.name)
        blog.save()

        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):

    model = Blog
    form_class = BlogForm
    # fields = ["title", "content", "image", "is_published"]
    extra_context = {"title": "Изменить"}
    # success_url = reverse_lazy("blog:blog_list") # Заменили на метод get_success_url()

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        """После успешного редактирования записи
        необходимо перенаправлять пользователя на просмотр этой статьи."""
        return reverse("blog:blog_detail", args=[self.kwargs.get("pk")])


    def get_form_class(self):
        """ Открываем форму, зависящую от уровня доступа пользователя"""
        user = self.request.user
        # Для Менеджера
        if user.has_perm('blog.can_reset_published'):
            return BlogManagerForm
        else:
            # для всех остальных
            return BlogForm

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy("blog:blog_list")
    extra_context = {"title": "Удалить"}
