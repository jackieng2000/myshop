from django.contrib import admin
# from .models import Category, Product
from .models import Studio, Booking, TimeSlot

@admin.register(Studio)
class StudioAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'address', 'photo', 'capacity')
    list_editable = ['district', 'address', 'photo', 'capacity']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('studio', 'date', 'start_time', 'end_time', 'guests')
    list_editable = ['start_time', 'end_time', 'guests']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('studio', 'date', 'start_time', 'end_time', 'is_available')
    list_editable = ['start_time', 'end_time', 'is_available']


   