from django.contrib import admin

from order_bot.models import Client, Master, Procedure, Salon, Appointment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = ('name', 'phone_number')
    list_display = ('name', 'phone_number')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    fields = ('name', 'service', 'phone_number')
    list_display = ('name', 'service', 'phone_number')


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    fields = ('title', 'price')


@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    fields = ('title', 'address')
    list_display = ('title', 'address')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    fields = ('date', 'salon', 'client', 'master', 'payment')
    list_display = ('date', 'salon', 'client', 'master', 'payment')
    readonly_fields = ('payment',)
