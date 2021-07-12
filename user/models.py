from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers import upload_to
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password=None, **kwargs):
        if not email:
            raise ValueError(_('Email must be provided'))
        elif not first_name:
            raise ValueError(_('First name must be provided'))
        elif not last_name:
            raise ValueError(_('Last name must be provided'))
        elif not date_of_birth:
            raise ValueError(_('Date of birth must be provided'))
        elif not password:
            raise ValueError(_('Password must be provided'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,
                         date_of_birth, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if kwargs.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    gender_choices = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    email = models.EmailField(_("Email"), max_length=254, unique=True)
    first_name = models.CharField(_("First Name"), max_length=50)
    last_name = models.CharField(_("Last Name"), max_length=50)
    date_of_birth = models.DateField(
        _("Date of Birth"), auto_now=False, auto_now_add=False)
    gender = models.CharField(
        _("Gender"), choices=gender_choices, max_length=50, default="Male")
    is_active = models.BooleanField(_("Is Active"), default=True)
    is_staff = models.BooleanField(_("Is Staff"), default=False)
    follows = models.ManyToManyField("self", verbose_name=_(
        "Followers"), symmetrical=False, through="followers.Followers",
        through_fields=("follower", "following"), related_name='followed_by')
    profile_picture = models.ImageField(
        _("Profile picture"),
        upload_to=upload_to, height_field=None, width_field=None, max_length=None, null=True)
    profile_updated_at = models.DateTimeField(
        _("Profile Update At"), auto_now=False, auto_now_add=False, null=True)
    is_private_profile = models.BooleanField(
        _("Is Private profile"), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email


class PasswordReset(models.Model):
    verification_key = models.CharField(
        _("Verification Key"), max_length=50, unique=True)
    user_id = models.OneToOneField(
        User, verbose_name=_("User Id"), on_delete=models.CASCADE)
