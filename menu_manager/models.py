import uuid
from django.db import models
from django.utils import timezone



class UUIDPrimaryKey(models.Model):
    """
    An abstract base class model that provides
    primary key id as uuid.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Option(UUIDPrimaryKey):
    meal = models.CharField(
        max_length=64,
    )
    created_date = models.DateTimeField(
            default=timezone.now)

    def __str__(self):
        return self.meal


class  Menu(UUIDPrimaryKey):
    start_date = models.DateField(
        'start date',
        db_index=True,
        unique=True,
    )
    options = models.ManyToManyField(
        Option,
        related_name='options',
    )
    is_sent = models.BooleanField(
        default=False,
    )


class Employee(UUIDPrimaryKey):
    user_id = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        )
    name = models.CharField(
        'name',
        max_length=80
    )
    email = models.EmailField(
        'e-mail',
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'


class  Answer(UUIDPrimaryKey):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    menu_option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name='answers',
        blank=True,
        null=True,
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    comentaries = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
