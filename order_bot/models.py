from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    """
    Клиент.
    """

    name = models.CharField(
        'ФИО',
        max_length=32
    )
    phone_number = PhoneNumberField(
        'Телефон',
        max_length=12,
        unique=True
    )

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name} (id: {self.id})'


class Master(models.Model):
    """
    Мастер салона красоты.
    """

    name = models.CharField(
        'ФИО',
        max_length=32
    )
    service = models.ForeignKey(
        'Procedure',
        related_name='masters',
        on_delete=models.SET_NULL,
        verbose_name='Услуга мастера',
        null=True
    )
    phone_number = PhoneNumberField(
        'Телефон',
        max_length=12,
        unique=True
    )

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return f'{self.name} (id: {self.id})'


class Procedure(models.Model):
    """
    Услуга салона.
    """

    title = models.CharField(
        'Название процедуры',
        max_length=32
    )
    price = models.DecimalField(
        'Цена процедуры',
        decimal_places=2,
        max_digits=8,
        default=0
    )

    class Meta:
        verbose_name = 'Процедура'
        verbose_name_plural = 'Процедуры'

    def __str__(self):
        return self.title


class Salon(models.Model):
    """
    Салон.
    """

    title = models.CharField(
        'Название салона',
        max_length=32
    )
    address = models.TextField(
        'Адрес салона',
        max_length=100
    )

    class Meta:
        verbose_name = 'Салон'
        verbose_name_plural = 'Салоны'

    def __str__(self):
        return self.title


class Appointment(models.Model):
    """
    Запись к мастеру (Расписание).
    """

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Клиент'
    )
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Мастер'
    )
    salon = models.ForeignKey(
        Salon,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Салон'
    )
    date = models.DateTimeField(
        'Дата приёма'
    )
    payment = models.BooleanField(
        'Оплата процедуры',
        default=False
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'Прием {self.client}'
