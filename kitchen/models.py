from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(User):
    question_1 = models.CharField(max_length=200, null=False)
    answer_1 = models.CharField(max_length=200, null=False)
    question_2 = models.CharField(max_length=200, null=False)
    answer_2 = models.CharField(max_length=200, null=False)
    is_provider = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# class Eater(models.Model):
#     # first name, last name, email, password are all inheritied from User
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50, null=False)
#     last_name = models.CharField(max_length=50, null=False)
#     question_1 = models.CharField(max_length=200, null=False)
#     answer_1 = models.CharField(max_length=200, null=False)
#     question_2 = models.CharField(max_length=200, null=False)
#     answer_2 = models.CharField(max_length=200, null=False)
#     is_provider = models.BooleanField(null=False)
#     # TODO: associate kitchen with provider if provider
#     def __str__(self):
#         return self.user.username

# class Provider(Eater):
#     def __str__(self):
#         return self.username


class Kitchen(models.Model):
#    WORKING_DAYS = (
#        ('Monday', 'Monday'),
#        ('Tuesday',  'Tuesday'),
#        ('Wednesday', 'Wednesday'),
#        ('Thursday', 'Thursday'),
#        ('Friday', 'Friday'),
#        ('Saturday', 'Saturday'),
#        ('Sunday', 'Sunday'),
#        )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50, null=False)
#    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    open_time = models.CharField(max_length=10, null=False)
    close_time = models.CharField(max_length=10, null=False)
    image = models.ImageField(upload_to='img/',  default='img/no_image.png')
    working_days = models.CharField(max_length=50, null=False)
    # TODO: Menu

    def __str__(self):
        return self.name

"""
class Menu(models.Model):
    pass

"""
class Food(models.Model):
    name = models.CharField(max_length=50, null=False)
    diet = models.CharField(max_length=7, choices=(('Veg','Veg'),('Non-Veg','Non-Veg')))
    price = models.FloatField(null=False)
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.SET_NULL, null=True, blank=True)
    food = models.ForeignKey(Food, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity