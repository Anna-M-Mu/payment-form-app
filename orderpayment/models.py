from django.db import models
    
class Item(models.Model):
    CURRENCY_CHOICES = [
        ('usd', 'USD - US Dollar'),
        ('eur', 'EUR - Euro'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')
    
    @property
    def price_in_main_unit(self):
        return int(self.price / 100)

    def __str__(self):
        return f"{self.name} ({self.currency.upper()})"


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent_off = models.PositiveIntegerField(help_text="Percentage off (e.g., 10 for 10%)")
    stripe_coupon_id = models.CharField(max_length=255, blank=True, null=True)

class Tax(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField(help_text="Tax percentage (e.g., 10 for 10%)")
    stripe_tax_id = models.CharField(max_length=255, blank=True, null=True) 

class Order(models.Model):
    items = models.ManyToManyField(Item)
    total_price = models.PositiveIntegerField(default=0)
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def calculate_total_price(self):
        print(f"Items in the order: {self.items.all()}")
        return sum(item.price for item in self.items.all())

    def update_total_price(self):
        """This method should be called explicitly after the order is saved."""
        self.total_price = self.calculate_total_price()
        self.save(update_fields=['total_price'])
    
    def add_random_tax_and_discount(self):
        self.discount = Discount.objects.order_by("?").first()
        self.tax = Tax.objects.order_by("?").first()
        self.save(update_fields=["discount", "tax"])
        
    def get_discount_amount(self):
        if self.discount:
            percent = self.discount.percent_off
            return self.total_price*percent/100
        return 0
    
    def get_tax_amount(self):
        if self.tax:
            percent = self.tax.percentage
            return self.total_price*percent/100
        return 0
    
    @property
    def total_price_in_main_unit(self):
        return int(self.total_price / 100)
    
    def __str__(self):
        return f"Order #{self.id}"