from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# менеджер нужен для переопределения настройки моделей юзера и суперюзера
class MyUserManager(BaseUserManager):
    # создается только через терминал (python manage.py createsuperuser)
    def create_superuser(self, email, password, **extrafields):
        # проверка на введение email
        if not email:
            raise ValueError('Email isn\'t provided!')
        # перевод введенного email в валидный вид
        email = self.normalize_email(email=email)
        # создание 'пустого юзера', ему будут добавляться валидные данные и только потом он будет записан в бд
        user = self.model(email=email, **extrafields)
        # проверка на введение пароля
        if not password:
            raise ValueError('Password isn\'t provided!')
        # установление пароля в модель юзера
        user.set_password(password)
        # указание, что юзер является staff
        user.is_staff = True
        # юзер актывный
        user.is_active = True
        # указание, что юзер является superuser
        user.is_superuser = True
        # сохранение юзера в бд
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extrafields):
        # проверка на введение email
        if not email:
            raise ValueError('Email isn\'t provided!')
        # перевод введенного email в валидный вид
        email = self.normalize_email(email=email)
        # создание 'пустого юзера', ему будут добавляться валидные данные и только потом он будет записан в бд
        user = self.model(email=email, **extrafields)
        # проверка на введение пароля
        if not password:
            raise ValueError('Password isn\'t provided!')
        # установление пароля в модель юзер
        user.set_password(password)
        # юзер не является staff и superuser (но если хотите, можно указать)
        # сохранение юзера в бд
        user.save(using=self._db)
        return user

# Модель юзера (user, superuser)
class MyUser(AbstractUser):
    # новые поля
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50, unique=True)
    # если нужна активация через почту, то default нужно ставить на false, и при активации менять на true
    is_active = models.BooleanField(default=True)

    # указание нашего менеджера
    objects = MyUserManager()

    # переопределение главного поля на email
    USERNAME_FIELD = 'email'
    # запись всех обязательных полей кроме sername, email, password
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username