from django.db import models


class Blog(models.Model):
    """Класс информации о записях"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое', blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', blank=True, null=True, upload_to='blog/image/')
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True, blank=True, null=True)
    publication = models.BooleanField(verbose_name='признак публикации', default=False, blank=True, null=True)
    show_counted = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0, blank=True, null=True)

    def __str__(self):
        """Магический метод, возвращающий название блога"""
        return self.title

    class Meta:
        """Класс метаданных для записей"""
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ['id']
        db_table = 'blog'
