from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
import pycountry

class MyAccountManager(BaseUserManager):

    def _validate_required(self, fields):
        for name, value in fields.items():
            if not value:
                raise ValueError(f"{name} is required")

    def create_user(
        self,
        username,
        phone_number,
        first_name,
        last_name,
        email,
        country,
        password=None,
    ):

        fields = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }

        self._validate_required(fields)

        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("wrong email format")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, email, username, first_name, last_name, password, phone_number, country
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number= phone_number , 
            country = country ,
            password = password ,
        )
        user.set_password(password)

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    @staticmethod
    def get_country():
        countries: list = list(pycountry.countries)
        country_choices = [(country.alpha_2, country.name) for country in countries]
        return country_choices

    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    phone_number = PhoneNumberField(unique=True)
    country = models.CharField(max_length=2, choices=get_country(), default="EG")

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "country",
        "phone_number",
    ]
    
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True
