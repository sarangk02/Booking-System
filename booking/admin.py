from django.contrib import admin
from . import models

admin.site.register(models.CustomUser) # register the CustomUser model
admin.site.register(models.Slot) # register the Slot model
admin.site.register(models.DeletedSlot) # register the DeletedSlot model