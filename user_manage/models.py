from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from PIL import Image

# Create your models here.

class User(AbstractUser):
	# Override default username field
	username = None

	# New fields
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)

	# Define new username field
	USERNAME_FIELD = 'email'

	# Define required user fields
	REQUIRED_FIELDS = ['first_name', 'last_name']

	objects = CustomUserManager()

	# Getter methods
	def get_email(self):
		return self.email

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	# To-string method
	def __str__(self):
		return self.get_full_name()