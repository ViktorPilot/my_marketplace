from django.views.generic import CreateView
from django.urls import reverse_lazy

from config.settings import EMAIL_HOST_USER
from users.forms import CustomCreationForm, UserAuthenticationForm
from users.models import CustomUser
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail


class RegisterView(CreateView):
    model = CustomUser
    form_class = CustomCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        subject = 'Приветствие от MyMarketplace!'
        message = f'Вы успешно зарегистрировались на сайте MyMarketplace!'
        send_mail(subject=subject, message=message, from_email=EMAIL_HOST_USER, recipient_list=[user.email,])
        return super().form_valid(form)

class CustomLoginView(LoginView):
    model = CustomUser
    form_class = UserAuthenticationForm
    template_name = 'users/login.html'
