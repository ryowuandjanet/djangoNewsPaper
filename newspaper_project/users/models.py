from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.crypto import get_random_string

class CustomUser(AbstractUser):
	age = models.PositiveIntegerField(default=0)

class EmailVerification(models.Model):
	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE
	)
	token = models.CharField(max_length=64)
	created_at = models.DateTimeField(auto_now_add=True)
	is_verified = models.BooleanField(default=False)

	def generate_token(self):
		self.token = get_random_string(64)
		self.save()
