from django.shortcuts import render
from .models import Article


def articles_list(request):
    template = 'articles/articles_list.html'
    
    # 1. Получаем все статьи из базы данных
    # 2. Используем prefetch_related для оптимизации (чтобы не было N+1 запросов к тегам)
    # 3. Сортируем по заголовку (так как поля published_at у нас нет)
    articles = Article.objects.prefetch_related('tags').order_by('title')
    
    # Передаем статьи в контекст под ключом 'object_list' (стандартное имя для ListView/шаблонов)
    context = {
        'object_list': articles
    }
    
    return render(request, template, context)
