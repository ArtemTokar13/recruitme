from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from datetime import datetime

from django.utils import timezone

USERTYPE_CHOICE = [
    ('OJ', 'Open to jobs'),
    ('HJ', 'Hires'),
]

APPLY_STATE = [
    ('RJ', 'Rejected'),
    ('IP', 'In process'),
]

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, password=None):
        """Creating user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)  # Making second half of email address to lowercase
        user = self.model(email=email)  # Creating user model object

        user.set_password(password)  # To make sure that password is incripted (set password to a hash)
        user.save(using=self._db)  # Standard procedure in Django of saving model in db

        return user

    def create_superuser(self, email, password):
        """Creating superuser (admin) profile"""
        user = self.create_user(email, password=password)

        user.is_superuser = True  # Standard field from Django
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Model for user profile. Rewriting custom (standard) Django user model in case to be able change it in the future"""
    email = models.EmailField(max_length=255, unique=True)
    hiring_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    company_name = models.CharField(max_length=255, null=True)
    registration_date = models.DateTimeField(default=datetime.now, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    user_type = models.CharField(max_length=20, choices=USERTYPE_CHOICE, default='OJ')

    objects = UserProfileManager()  # Creating user profile manager for create and control users with Command Line Interface tool

    USERNAME_FIELD = 'email'  # Changing username for email (required by default)
    REQUIRED_FIELDS = []  # Adding name to required fields

    def get_full_name(self):
        """Reassignment of full name in custom model"""
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        """Reassignment of short name in custom model"""
        return self.first_name


class SkillTag(models.Model):
    """Skills or requirements"""
    tagname = models.CharField(max_length=255)
    owner = models.ManyToManyField(UserProfile)

    def __str__(self):
        return self.tagname


class WorkerProfile(models.Model):
    """Model for worker`s profile"""
    workername = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    introduction = models.CharField(max_length=500)
    resume = models.FileField(upload_to='recruitme/cv/profiles/%Y/%m/%d', blank=True, null=True)

    def __str__(self):
        return str(self.workername.first_name) + ' ' + str(self.workername.last_name) + ' email: ' + str(self.workername.email)


class JobProfile(models.Model):
    """Model for job position"""
    employername = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    offer_name = models.CharField(max_length=255)
    description = models.CharField(max_length=511)

    def __str__(self):
        return self.offer_name


class Requirements(models.Model):
    """Model for job requirements"""
    job = models.ManyToManyField(JobProfile)
    rname = models.CharField(max_length=255)

    def __str__(self):
        return self.rname


class Apply(models.Model):
    """Job apply model"""
    job = models.ForeignKey(JobProfile, on_delete=models.CASCADE)
    worker = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='recruitme/cv/applies/%Y/%m/%d', blank=True, null=True)
    coverletter = models.CharField(max_length=511, blank=True)
    apply_date = models.DateTimeField(default=timezone.now)
    state = models.CharField(max_length=20, choices=APPLY_STATE, blank=True)
    employer_comment = models.CharField(max_length=511, blank=True)
    read = models.BooleanField(default=False)
    read_date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-apply_date']

    def __str__(self):
        return str(self.worker) + ' ' + str(self.job)