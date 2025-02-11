from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from posts.models import Post, Comment
from posts.forms import PostForm, CommentForm
from django.core.paginator import Paginator


class CommentListView(ListView):
    model = Comment
    template_name = 'posts/comment_list.html'
    context_object_name = 'comments'
    paginate_by = 25

    def get_queryset(self):
        queryset = Comment.objects.all().order_by('-created_at')  # Сортировка по дате
        return queryset

    def get_ordering(self):
        order_by = self.request.GET.get('order_by', '-created_at')  # Параметр для сортировки
        return order_by


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        # Получаем все посты и применяем сортировку
        order_by = self.request.GET.get('order_by', '-created_at')
        return Post.objects.all().order_by(order_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все посты
        posts_list = self.get_queryset()

        # Пагинация
        paginator = Paginator(posts_list, 25)  # 25 на странице
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Добавляем в контекст посты и дополнительные данные
        context['posts'] = page_obj
        context['order_by'] = self.request.GET.get('order_by', '-created_at')
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_form.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Комментарий не может быть пустым.")
        return redirect(reverse("post_detail", kwargs={"pk": self.kwargs["post_id"]}))

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.kwargs['post_id']})
