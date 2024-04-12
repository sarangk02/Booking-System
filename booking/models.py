from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin, AbstractBaseUser
from django.utils import timezone

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

class CustomUser(AbstractBaseUser, PermissionsMixin):
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

    class Meta:
        ordering = ['username']
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username


class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    # custom image name while saving
    def payment_image_path(instance, filename):
        date = instance.date.strftime("%d")+'-'+instance.date.strftime("%m")+'-'+instance.date.strftime("%y")
        start_time = instance.start_time.strftime('%H')
        end_time = instance.end_time.strftime('%H')
        return f'payment_images/{date}_from_{start_time}_to_{end_time}_{instance.user.username}_{filename}'
    payment_image = models.ImageField(upload_to=payment_image_path, blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_time = models.DateTimeField(default=timezone.now, editable=False)
    is_booked = models.BooleanField(default=False)
    is_booked_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['request_time']
        verbose_name = 'slot'
        verbose_name_plural = 'slots'

    def __str__(self):
        return str(self.date.strftime('%D')) + ' | ' + str(self.start_time.strftime('%H')) + ' to ' + str(self.end_time.strftime('%H')) + ' | ' + str(self.user)

# class DeletedSlot(models.Model):
#     id = models.AutoField(primary_key=True)
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     payment_image = models.ImageField(upload_to='payment_images/', blank=True, null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     request_time = models.DateTimeField(default=timezone.now, editable=False)
#     is_booked = models.BooleanField(default=False)
#     is_booked_time = models.DateTimeField(blank=True, null=True)
#     reason = models.TextField()

#     class Meta:
#         ordering = ['request_time']
#         verbose_name = 'deleted slot'
#         verbose_name_plural = 'deleted slots'

#     def __str__(self):
#         return str(self.date.strftime('%D')) + ' | ' + str(self.start_time.strftime('%H')) + ' to ' + str(self.end_time.strftime('%H')) + ' | ' + str(self.user)