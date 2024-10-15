from django.contrib import admin
from .models import CourseSession, MenuItem, Instructor

@admin.register(MenuItem)
class MenuitemAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'name', 'slug', 'image', 'available']
    list_editable = ['image', 'available',]
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'name', 'slug', 'image', 'available']
    list_editable = ['image', 'available',]
    prepopulated_fields = {'slug': ('name',)}   
    

@admin.register(CourseSession)
class CourseSessionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'quota', 'available']
    list_editable = ['quota', 'available',]
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        # Set the modified_by field to the current user's username
        obj.modified_by = request.user.username
        super().save_model(request, obj, form, change)
