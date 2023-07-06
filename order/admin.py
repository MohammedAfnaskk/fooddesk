from django.contrib import admin
from .models import*
from django.utils.html import format_html

# Register your models here.
admin.site.register(Wallet)
class OrderreturnAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'comment_display', 'image_display']
    
    def comment_display(self, obj):
        return obj.comment if obj.comment else ''
    comment_display.short_description = 'Comment'
    
    def image_display(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return format_html('<span style="color:red;">No Image</span>')
    image_display.short_description = 'Image'

admin.site.register(Orderreturn, OrderreturnAdmin)

