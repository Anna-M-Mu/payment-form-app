from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from .models import Item, Order, Discount, Tax

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "currency")
    search_fields = ("name",)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    readonly_fields = ("stripe_coupon_id",)
    list_display = ("id", "name", "percent_off")
    search_fields = ("name",)

@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    readonly_fields = ("stripe_tax_id",)
    list_display = ("id", "name", "percentage")
    search_fields = ("name",)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['items']

    def clean_items(self):
        items = self.cleaned_data.get('items', [])
        currencies = {item.currency for item in items}
        if len(currencies) > 1:
            raise ValidationError("All items must have the same currency.")        
        return items


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm

    readonly_fields = ("total_price", "discount", "tax")
    filter_horizontal = ("items",)
    list_display = ("id", "total_price", "discount", "tax")
    search_fields = ("id",)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        form.save_m2m() 
        obj.update_total_price()
        obj.add_random_tax_and_discount()

admin.site.register(Order, OrderAdmin)