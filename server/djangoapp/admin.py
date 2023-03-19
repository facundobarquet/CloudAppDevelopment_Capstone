from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.
# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [CarModelInline]

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)