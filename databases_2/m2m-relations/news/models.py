from django.db import models


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


class Scope(models.Model):
    """Промежуточная таблица связи Статья-Тег с дополнительным полем is_main"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Раздел')
    is_main = models.BooleanField(default=False, verbose_name='Основной раздел')

    class Meta:
        verbose_name = 'Связь'
        verbose_name_plural = 'Связи'
        unique_together = ('article', 'tag')pyth

    def __str__(self):
        return f"{self.article} - {self.tag}"