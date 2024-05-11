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
    username = models.CharField(max_length=255, unique=True)  # Username field
    name = models.CharField(max_length=255)  # User's name
    email = models.EmailField(max_length=255, unique=True)  # User's email address
    contact = models.CharField(max_length=10, unique=True)  # User's contact number
    emerg_name = models.CharField(max_length=255)  # Emergency contact name
    emerg_contact = models.CharField(max_length=10)  # Emergency contact number
    gender = models.CharField(max_length=1)  # User's gender
    email_verified = models.BooleanField(default=False)  # Email verification status
    contact_verified = models.BooleanField(default=False)  # Contact verification status
    is_staff = models.BooleanField(default=False)  # Staff status

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
    def payment_image_path(instance, filename):
        date = instance.date.strftime("%d")+'-'+instance.date.strftime("%m")+'-'+instance.date.strftime("%y")
        start_time = instance.start_time.strftime('%H')
        end_time = instance.end_time.strftime('%H')
        return f'payment_images/{date}_from_{start_time}_to_{end_time}_{instance.user.username}_{filename}'
    id = models.AutoField(primary_key=True)  # Slot ID
    date = models.DateField()  # Slot date
    start_time = models.TimeField()  # Slot start time
    end_time = models.TimeField()  # Slot end time
    payment_image = models.ImageField(upload_to=payment_image_path, blank=False, null=False)  # Payment image
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who booked the slot
    request_time = models.DateTimeField(default=timezone.now, editable=False)  # Slot booking request time
    is_booked = models.BooleanField(default=False)  # Slot booking status
    is_booked_time = models.DateTimeField(blank=True, null=True)  # Time when the slot was booked

    class Meta:
        ordering = ['request_time']
        verbose_name = 'slot'
        verbose_name_plural = 'slots'

    def __str__(self):
        return str(self.date.strftime('%D')) + ' | ' + str(self.start_time.strftime('%H')) + ' to ' + str(self.end_time.strftime('%H')) + ' | ' + str(self.user)

class DeletedSlot(models.Model):
    def payment_image_path(instance, filename):
        return ''
    id = models.AutoField(primary_key=True)  # Deleted slot ID
    date = models.DateField()  # Deleted slot date
    start_time = models.TimeField()  # Deleted slot start time
    end_time = models.TimeField()  # Deleted slot end time
    payment_image = models.ImageField(upload_to=payment_image_path, blank=True, null=True)  # Payment image (optional)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # User who booked the deleted slot
    request_time = models.DateTimeField(editable=False)  # Slot booking request time
    deletiontime = models.DateTimeField(default=timezone.now, editable=False)  # Slot deletion time
    reason = models.TextField()  # Reason for slot deletion

    class Meta:
        ordering = ['deletiontime']
        verbose_name = 'Deleted Slot'
        verbose_name_plural = 'Deleted Slots'

    def __str__(self):
        return str(self.date.strftime('%D')) + ' | ' + str(self.start_time.strftime('%H')) + ' to ' + str(self.end_time.strftime('%H')) + ' | ' + str(self.user)
