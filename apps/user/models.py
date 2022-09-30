# apps/user/models.py
# Django
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        if not email:
            raise ValueError("Users must have a email")
        
        user = self.model(
            email=email,
            name=name
        )

        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email=email,
            password=password,
            name=name
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=128,
        verbose_name="사용자 이메일",
        unique=True,
        )
    name = models.CharField(
        verbose_name="사용자명",
        max_length=30,
        blank=False
        )
    is_active = models.BooleanField(
        verbose_name=_('Is active'),
        default=True
        )
    date_joined = models.DateTimeField(
        verbose_name=_('Date joined'),
        default=timezone.now
        )

    objects = CustomUserManager()

    USERNAME_FIELD='email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)


    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser