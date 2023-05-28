from django.contrib import admin

from order_bot.models import Master, Procedure, Salon, Appointment, WorkTime, WorkDay, Promo


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    fields = ('name', 'service', 'phone_number')
    list_display = ('name', 'phone_number')
    list_filter = ('service',)


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    fields = ('title', 'price')
    ordering = ('id',)


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    fields = ('title', 'address', 'open_time', 'close_time', 'procedures', 'workers')
    list_display = ('title', 'address')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    fields = ('date', 'salon', 'name', 'phone_number', 'master', 'service', 'payment')
    list_display = ('date', 'salon', 'master', 'payment')
    readonly_fields = ('payment',)


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    fields = ('begin', 'end', 'worker', 'workplace')
    list_display = ('workplace', 'worker', 'begin', 'end')
    list_filter = ('workplace', 'worker')


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    fields = ('day', 'worktime')


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    fields = ('promo', 'status')
    list_filter = ('status',)
