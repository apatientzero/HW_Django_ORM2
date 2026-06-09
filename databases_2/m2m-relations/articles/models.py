from django.db import models
from django.core.exceptions import ValidationError


class Tag(models.Model):
    """Тематический раздел (тег)"""
    name = models.CharField(max_length=50, verbose_name='Название раздела')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Article(models.Model):
    """Новостная статья"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст статьи')
    image = models.ImageField(
        upload_to='articles/',
        null=True,
        blank=True,
        verbose_name='Изображение'
    )

    # Связь ManyToMany через промежуточную модель Scope
    tags = models.ManyToManyField(
        Tag,
        through='Scope',
        related_name='articles'
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_sorted_tags(self):
        """Возвращает теги: сначала основной, потом остальные по алфавиту"""
        scopes = self.scope_set.select_related('tag').all()
        main_tags = [s.tag for s in scopes if s.is_main]
        other_tags = sorted(
            [s.tag for s in scopes if not s.is_main],
            key=lambda t: t.name
        )
        return main_tags + other_tags


class Scope(models.Model):
    """Промежуточная таблица связи Статья-Тег с полем is_main"""
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='Статья'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Раздел'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Основной раздел'
    )

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
        unique_together = ('article', 'tag')

    def __str__(self):
        return f"{self.article} - {self.tag}"

    def clean(self):
        """Валидация: у статьи должен быть ровно один основной раздел"""
        if self.is_main:
            if not self.article.pk:
                return

            existing_main = Scope.objects.filter(
                article=self.article,
                is_main=True
            ).exclude(pk=self.pk).exists()

            if existing_main:
                raise ValidationError(
                    "У статьи уже есть основной раздел. "
                    "Основным может быть только один."
                )