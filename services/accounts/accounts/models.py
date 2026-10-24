import pyotp
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserProfile(TimestampModel):
    class Type(models.TextChoices):
        STUDENT = 'student', 'Студент'
        INSTRUCTOR = 'instructor', 'Инструктор'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(choices=Type.choices, max_length=20)
    totp_key = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.type})"

    def save(self, *args, **kwargs):
        if not self.totp_key:
            self.totp_key = pyotp.random_base32()
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()