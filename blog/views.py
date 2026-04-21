from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail

from blog.models import Blog


class BlogListView(ListView):
    """Класс контроллера списка записей"""
    model = Blog

    def get_queryset(self):
        """Метод отфильтровывающий записи по положительному типу публикации"""
        queryset = super().get_queryset().filter(publication=True)
        return queryset


class BlogDetailView(DetailView):
    """Класс контроллера детальной информации о записи"""
    model = Blog

    def get_object(self, queryset=None):
        """Метод, увеличивающий счетчик просмотра страницы записи при переходе на нее
        и отправляющий на почту сообщение при количестве просмотров 100"""
        self.object = super().get_object()
        self.object.show_counted += 1
        self.object.save()
        if self.object.show_counted == 100:
            send_mail('Поздравление!', f'Поздравляем! У Вас 100 просмотров блога {self.object.title}',
                      'viktorbukotin0@gmail.com', ['veterwind666@rambler.ru'])
        return self.object


class BlogCreateView(CreateView):
    """Класс контроллера создания новой записи"""
    model = Blog
    fields = ('title', 'content', 'image', 'publication', 'show_counted',)
    success_url = reverse_lazy("blog:home_blog")


class BlogUpdateView(UpdateView):
    """Класс контроллера обновления существующей записи"""
    model = Blog
    fields = ('title', 'content', 'image', 'publication', 'show_counted',)

    def get_success_url(self):
        """Метод для перехода на страницу записи после ее создания"""
        return reverse_lazy('blog:detail_blog', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Класс контроллера удаления записи"""
    model = Blog
    success_url = reverse_lazy("blog:home_blog")
