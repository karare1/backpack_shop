from django.contrib import admin
from .models import Order, OrderLine


class OrderLineAdminInline(admin.TabularInline):
    # Adds order line items in Django Admin
    model = OrderLine
    readonly_fields = ('line_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'delivery_cost', 'order_total',
                       'final_total', 'original_cart',
                       'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'final_total', 'original_cart',
                       'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'final_total',)

    # reverse chronological order
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
