from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(user_signed_up)
def create_profile(sender, request, user, **kwargs):
    # Check if a profile already exists for the user
    try:
        profile = user.user_profile
        # Update the existing profile if needed
        # profile.some_field = some_value
        profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=user)


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


