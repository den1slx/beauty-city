from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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
        return f'{self.id}) {self.title}'


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
    open_time = models.TimeField(
        verbose_name='Время открытия',
        null=True
    )
    close_time = models.TimeField(
        verbose_name='Время закрытия',
        null=True
    )
    procedures = models.ManyToManyField(
        'Procedure',
        related_name='salon',
        verbose_name='Оказываемые услуги'
    )
    workers = models.ManyToManyField(
        'Master',
        related_name='salon',
        verbose_name='Наши специалисты'
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

    name = models.CharField(
        'ФИО',
        max_length=32,
        null=True,
    )
    phone_number = PhoneNumberField(
        'Телефон',
        max_length=12,
        null=True,
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
    service = models.ForeignKey(
        'Procedure',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Процедура',
        null=True,
    )
    payment = models.BooleanField(
        'Предоплата процедуры',
        default=False
    )
    promo = models.BooleanField(
        default=False,
        null=True,
    )

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def __str__(self):
        return f'Прием {self.name} Телефон{self.phone_number}'


class WorkTime(models.Model):
    """
    Рабочее время мастера.
    """

    begin = models.TimeField(
        verbose_name='Начало смены'
    )
    end = models.TimeField(
        verbose_name='Конец смены'
    )
    worker = models.ForeignKey(
        'Master',
        related_name='worktime',
        verbose_name='Мастер',
        on_delete=models.CASCADE,
        null=True,
    )
    workplace = models.ForeignKey(
        'Salon',
        related_name='workplace',
        verbose_name='Место работы',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Рабочие смены'
        verbose_name_plural = 'Рабочие смены'

    def __str__(self):
        return f'С {self.begin} до {self.end}'


class WorkDay(models.Model):
    """
    Рабочий день мастера.
    """

    day = models.DateField(
        'Дата'
    )
    worktime = models.ManyToManyField(
        'WorkTime',
        related_name='worktime',
        verbose_name='Рабочие смены дня'
    )

    class Meta:
        verbose_name_plural = 'Рабочие дни'

    def __str__(self):
        return f'{self.day}'


class Promo(models.Model):
    promo = models.CharField(
        'Промокод',
        max_length=20
    )
    status = models.BooleanField(
        'Статус',
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Промокоды'
        verbose_name = 'Промокод'

    def __str__(self):
        return f'{self.promo} {self.status}'
