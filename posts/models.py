from django.db import models
from django.conf import settings
import bleach

ALLOWED_TAGS = ['b', 'i', 'u', 'a']
ALLOWED_ATTRIBUTES = {'a': ['href', 'title']}

class Post(models.Model):
    """Модель поста пользователя."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Автор поста."
    )
    text = models.TextField(help_text="Текст поста. Поддерживаются теги: b, i, u, a.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата последнего обновления.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        # self.author всегда экземпляр пользователя
        return f"{self.author} - {self.created_at:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs):
        """Очищает текст от опасных тегов и атрибутов перед сохранением."""
        self.text = bleach.clean(str(self.text), tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Модель комментария к посту, поддерживает древовидную структуру."""
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments",
        help_text="Пост, к которому относится комментарий."
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        help_text="Автор комментария."
    )
    text = models.TextField(help_text="Текст комментария.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания.")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True,
        related_name="replies", help_text="Родительский комментарий (для вложенности)."
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        # self.author и self.post всегда экземпляры моделей
        return f"Comment by {self.author} on post {self.post} at {self.created_at:%Y-%m-%d %H:%M}"
