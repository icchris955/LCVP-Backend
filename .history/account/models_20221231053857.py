import uuid
from PIL import Image
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


CHOICES_ACCOUNT_TYPE = (
    ("personal", "Personal"),
    ("business", "Business"),
)


class UserManager(BaseUserManager):
    """Define a model manager for a custom user"""

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email should be provided.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, nid, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, nid, phone, password, **extra_fields)

    def create_superuser(self, email, nid, phone, password=None, **extra_fields):
        """Create a superuser with NID,  email, phone and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, nid, phone, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(verbose_name="Name", max_length=255, blank=False, null=True)
    nid = models.CharField(
        verbose_name="National ID",
        max_length=16,
        unique=True,
        error_messages={
            "required": "Don't forget to add your National ID",
            "unique": "Someone else is using this National ID",
        },
    )
    email = models.EmailField(
        max_length=254,
        blank=False,
        null=True,
        unique=True,
        error_messages={
            "required": "Your email please!",
            "unique": "This Email address is already in use.",
        },
    )
    phone = models.CharField(
        verbose_name="Phone",
        max_length=12,
        unique=True,
        error_messages={
            "required": "Your phone number!",
            "unique": "There is someone else using this phone number.",
        },
    )
    password = models.CharField(verbose_name="Password", max_length=150, null=False)
    public_id = models.UUIDField(
        unique=True, primary_key=False, default=uuid.uuid4, editable=False
    )
    account_type = models.CharField(
        choices=CHOICES_ACCOUNT_TYPE, default="personal", max_length=250, null=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"

    REQUIRED_FIELDS = ["nid", "name", "email"]

    def __str__(self):
        return f"(%s) %s" % (self.name, self.nid)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default="default.jpg", upload_to=f"profiles/{user.name}")

    def __str__(self):
        return f"Profile for {self.user.nid}"

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


"""
User additional info: address, province, district, sector, about me, first and last name
"""


class AdditionalInfo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250, null=True)
    last_name = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=250, null=True)
    province = models.CharField(max_length=250, null=True)
    district = models.CharField(max_length=250, null=True)
    sector = models.CharField(max_length=250, null=True)
    about = models.TextField(verbose_name="About Me", max_length=250, null=True)

    def __str__(self):
        return f"%s" % self.user.name


class Rate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(default=0, null=True)

    def __str__(self):
        return f"Rating #%s" % self.id
