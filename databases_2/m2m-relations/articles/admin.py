from django.contrib import admin
from .models import Article, Tag, Scope



class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 1
    min_num = 1
    verbose_name = 'Раздел'
    verbose_name_plural = 'Разделы статьи'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_tags')
    inlines = [ScopeInline]

    def get_tags(self, obj):
        """Метод для отображения списка тегов в админке"""
        return ", ".join([scope.tag.name for scope in obj.scope_set.all()])

    get_tags.short_description = 'Разделы'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ('article', 'tag', 'is_main')