from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from django.core.paginator import Paginator


class CommentListView(ListView):
    """Список всех комментариев с пагинацией."""
    model = Comment
    template_name = 'posts/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 25

    def get_queryset(self):
        """Возвращает отсортированный по дате список комментариев."""
        order_by = self.request.GET.get('order_by', '-created_at')
        return Comment.objects.all().order_by(order_by)


class PostListView(ListView):
    """Список всех постов с пагинацией и сортировкой."""
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 25

    def get_queryset(self):
        """Возвращает отсортированный по дате список постов."""
        order_by = self.request.GET.get('order_by', '-created_at')
        return Post.objects.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        """Добавляет в контекст текущий порядок сортировки."""
        context = super().get_context_data(**kwargs)
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        return context


class PostDetailView(DetailView):
    """Детальный просмотр поста."""
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    """Создание нового поста (только для авторизованных пользователей)."""
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        """Устанавливает текущего пользователя автором поста."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Создание комментария к посту (только для авторизованных пользователей)."""
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def form_valid(self, form):
        """Устанавливает автора и пост для комментария."""
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def form_invalid(self, form):
        """Показывает ошибку, если форма невалидна."""
        messages.error(self.request, "Комментарий не может быть пустым.")
        return redirect(reverse("post_detail", kwargs={"pk": self.kwargs["post_id"]}))

    def get_success_url(self):
        """После успешного создания комментария возвращает на страницу поста."""
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs['post_id']})
