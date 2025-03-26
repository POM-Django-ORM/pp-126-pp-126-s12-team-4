from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone
import time

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'admin'),
)


class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    middle_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=128)
    created_at = models.IntegerField(default=lambda: int(timezone.now().timestamp()), editable=False)
    updated_at = models.IntegerField(default=lambda: int(timezone.now().timestamp()))
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return f"CustomUser(id={self.id})"

    @staticmethod
    def get_by_id(user_id):
        return CustomUser.objects.filter(id=user_id).first()

    @staticmethod
    def get_by_email(email):
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def delete_by_id(user_id):
        user = CustomUser.objects.filter(id=user_id)
        if user.exists():
            user.delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None):
        if len(first_name or '') > 20 or len(middle_name or '') > 20 or len(last_name or '') > 20:
            return None
        if '@' not in email or '.' not in email:
            return None
        if CustomUser.objects.filter(email=email).exists():
            return None

        return CustomUser.objects.create(
            email=email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name
        )

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role': self.role,
            'is_active': self.is_active,
        }

    def update(self, first_name=None, last_name=None, middle_name=None, password=None, role=None, is_active=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if middle_name:
            self.middle_name = middle_name
        if password:
            self.password = password
        if role is not None:
            self.role = role
        if is_active is not None:
            self.is_active = is_active
        self.updated_at = int(timezone.now().timestamp())
        self.save()

    @staticmethod
    def get_all():
        return CustomUser.objects.all()

    def get_role_name(self):
        return dict(ROLE_CHOICES).get(self.role, 'unknown')
