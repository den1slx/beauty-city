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
    prepay = models.BooleanField(default=False, null=True)

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
    service = models.ManyToManyField(
        'Procedure',
        related_name='masters',
        verbose_name='Услуги мастера',
        blank=True,
    )
    phone_number = PhoneNumberField(
        'Телефон',
        max_length=12,
        unique=True
    )
    worktime = models.ManyToManyField('WorkTime', verbose_name='Время работы', related_name='master', blank=True)

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
    open_time = models.TimeField(null=True, verbose_name='Время открытия')
    close_time = models.TimeField(null=True, verbose_name='Время закрытия')
    procedures = models.ManyToManyField('Procedure', verbose_name='Оказываемые услуги', related_name='salon')
    workers = models.ManyToManyField('Master', verbose_name='Наши специалисты', related_name='salon')
    days = models.ManyToManyField('WorkDay', verbose_name='Рабочие дни', related_name='salon')

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
        'Предоплата процедуры',
        default=False
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'Прием {self.client}'


class WorkTime(models.Model):
    begin = models.TimeField(verbose_name='Начало смены')
    end = models.TimeField(verbose_name='Конец смены')
    worker = models.OneToOneField(
        'Salon',
        on_delete=models.CASCADE,
        verbose_name='Место работы',
        related_name='worktime',
        null=True,
    )

    class Meta:
        verbose_name = 'Рабочие смены'
        verbose_name_plural = 'Рабочие смены'

    def __str__(self):
        return f'С {self.begin} до {self.end}'


class WorkDay(models.Model):
    day = models.DateField()
    worktime = models.ManyToManyField('WorkTime', verbose_name='Рабочие смены дня', related_name='worktime')

    class Meta:
        verbose_name_plural = 'Рабочие дни'

    def __str__(self):
        return f'{self.day}'
