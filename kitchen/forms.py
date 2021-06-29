from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Customer, Order


class KitchenForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    open_time = forms.CharField(max_length=10, required=True)
    close_time = forms.CharField(max_length=10, required=True)
    image = forms.ImageField(required=False)
    WORKING_DAYS = (
        ('Monday', 'Monday'),
        ('Tuesday',  'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    working_days = forms.MultipleChoiceField(choices=WORKING_DAYS, required=True, widget=forms.CheckboxSelectMultiple)

# class FoodForm(forms.ModelForm):
#     class Meta:
#         model = Food
#         fields = '__all__'
#         exclude = ['kitchen']

class NewCustomerForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    question1 = forms.CharField(label='Enter security question 1')
    answer1 = forms.CharField(label='Enter security answer 1', widget=forms.PasswordInput)
    question2 = forms.CharField(label='Enter security question 2')
    answer2 = forms.CharField(label='Enter security answer 1', widget=forms.PasswordInput)
    # is_provider = forms.BooleanField()
    is_provider = forms.BooleanField(required=False)


    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = Customer.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Customer.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def clean_question1(self):
        question1 = self.cleaned_data['question1'].lower()
        return question1

    def clean_question2(self):
        question1 = self.cleaned_data['question2'].lower()
        return question1

    def clean_answer1(self):
        answer1 = self.cleaned_data['answer1'].lower()
        return answer1

    def clean_answer2(self):
        answer2 = self.cleaned_data['answer2'].lower()
        return answer2

    def clean_is_provider(self):
        is_provider = self.cleaned_data['is_provider']
        return is_provider


    def save(self, commit=True):
        user = Customer.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )

        user.save()

        customer = Customer(
            user,
            self.cleaned_data['question1'],
            self.cleaned_data['question2'],
            self.cleaned_data['answer1'],
            self.cleaned_data['answer2'],
            self.cleaned_data['is_provider'],
        )

        return customer


# class EaterCreationForm(forms.Form):
#     username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
#     email = forms.EmailField(label='Enter email')
#     password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
#
#     def clean_username(self):
#         username = self.cleaned_data['username'].lower()
#         r = User.objects.filter(username=username)
#         if r.count():
#             raise  ValidationError("Username already exists")
#         return username
#
#     def clean_email(self):
#         email = self.cleaned_data['email'].lower()
#         r = User.objects.filter(email=email)
#         if r.count():
#             raise  ValidationError("Email already exists")
#         return email
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Password don't match")
#
#         return password2
#
#     def save(self, commit=True):
#         user = User.objects.create_user(
#             self.cleaned_data['username'],
#             self.cleaned_data['email'],
#             self.cleaned_data['password1']
#         )
#
#         return user
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddItemForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'postal_code', 'city']