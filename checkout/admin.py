from django.contrib import admin
from .models import Order, OrderLine
# Register your models here.


class OrderLineAdminInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ('line_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'final_total',)

    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'final_total',)

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'final_total',)

    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)