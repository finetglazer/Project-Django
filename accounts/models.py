from djongo import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email)
        user.set_password(password)  # This will hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    # You do not need to explicitly define the password field here
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # To allow admin login (optional)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Fields required to create a superuser

    objects = UserAccountManager()

    def __str__(self):
        return self.username
