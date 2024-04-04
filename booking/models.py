from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractUser

# create custom user model here

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contact = models.CharField(max_length=10, unique=True)
    emerg_name = models.CharField(max_length=255)
    emerg_contact = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    email_verified = models.BooleanField(default=False)
    contact_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username