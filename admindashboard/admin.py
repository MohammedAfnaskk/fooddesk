
from django.contrib import admin
from admindashboard.models import *


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Product)
admin.site.register(Category)
