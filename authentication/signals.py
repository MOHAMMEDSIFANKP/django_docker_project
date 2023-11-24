from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import *
import qrcode
import hashlib
from io import BytesIO
from django.core.files import File
from django.conf import settings
from decouple import config
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_id = str(instance.id)
        secret_key = settings.SECRET_KEY 
        registration_time = instance.date_joined.timestamp()
        token = f"{user_id}:{registration_time}:{secret_key}"
        secure_token = hashlib.sha256(token.encode()).hexdigest()
        base_url = config('base_url')
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        redirect_url = f'{base_url}QrProfileView/{secure_token}/{user_id}/'
        qr.add_data(redirect_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to user's profile
        img_buffer = BytesIO()
        img.save(img_buffer)
        img_filename = f'qrcode_{instance.username}.png'
        user_profile = UserProfile.objects.get_or_create(user=instance)[0]
        user_profile.qrcode.save(img_filename, File(img_buffer))
        user_profile.save()