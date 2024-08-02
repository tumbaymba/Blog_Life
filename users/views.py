from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from users.services import create_payment_session
from django.urls import reverse, reverse_lazy
from users.forms import RegisterForm, UserProfileForm
from django.shortcuts import redirect, render
from users.models import User


class RegisterView(CreateView):
    """Регистрация пользователя"""
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        """Валидная форма регистрации пользователя"""
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return redirect('users:verify_message')

    def get_success_url(self):
        """Получение URL для перенаправления после успешной регистрации"""
        return reverse('users:verify_message')


class ProfileView(UpdateView):
    """Профиль пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:success_profile')

    def get_object(self, queryset=None):  # тем самым уходим от привязки с pk
        return self.request.user


def create_subscription(request):
    """Создание оплаты подписки"""
    if request.user.is_authenticated:
        user = request.user
        if not user.is_subscribed:
            session = create_payment_session(request)
            return redirect(session.url)
        else:
            messages.info(request, 'У вас уже есть активная подписка.')
            return redirect('blog:index')
    else:
        messages.error(request,
                       'Пожалуйста, зарегистрируйтесь и войдите в личный профиль на сайте, и повторите попытку!')
        return redirect('users:login')


def cancel_subscription(request):
    """URL для перенаправления в случае отмены платежа"""
    return render(request, 'users/cancel_payment.html')


def success_subscription(request):
    """Обработка оплаты подписки"""
    if request.user.is_authenticated:
        user = request.user
        user.is_subscribed = True
        user.save()
        messages.success(request, 'Подписка успешно оформлена!')
        return redirect('blog:index')

    else:
        messages.error(request, 'Что-то пошло не так, повторите попытку.')
        return redirect('users:login')
