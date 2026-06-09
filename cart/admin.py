from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'total', 'status', 'created_at', 'whatsapp_sent']
    list_filter = ['status', 'whatsapp_sent', 'created_at']
    search_fields = ['order_id', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_id', 'created_at', 'updated_at', 'total_items_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'status', 'whatsapp_sent')
        }),
        ('Customer Details', {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone')
        }),
        ('Order Items', {
            'fields': ('items', 'total_items_count'),
            'description': 'Items are stored in JSON format'
        }),
        ('Payment', {
            'fields': ('subtotal', 'delivery_fee', 'total')
        }),
        ('Additional Info', {
            'fields': ('notes', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_items_count(self, obj):
        return obj.total_items_count()
    total_items_count.short_description = 'Total Items'
