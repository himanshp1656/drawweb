from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    referral_link = models.CharField(max_length=100, blank=True, unique=True)
    coin=models.IntegerField(default=0)
    refralcoin=models.IntegerField(default=0)
    def __str__(self):
        return self.user.username

    def generate_referral_link(self):
        unique_id = str(uuid.uuid4())[:8]  # Generate a unique ID
        self.referral_link = unique_id
        self.save()

    def save(self, *args, **kwargs):
        if not self.referral_link:
            self.generate_referral_link()
        super().save(*args, **kwargs)

from django.core.exceptions import ValidationError
class prize(models.Model):
    prize=models.CharField(max_length=200)
    def __str__(self):
        return self.prize
    def save(self, *args, **kwargs):
        # Ensure only one instance of Prize exists
        if prize.objects.exists() and not self.pk:
            raise ValidationError("Only one prize can exist.")
        super().save(*args, **kwargs)
    
class WinnerList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prizewon = models.ForeignKey(prize, on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username