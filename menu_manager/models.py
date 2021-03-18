import uuid
from django.db import models
from django.utils import timezone
# Create your models here.


class UUIDPrimaryKey(models.Model):
    """
    An abstract base class model that provides
    primary key id as uuid.
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class MenuOptions(UUIDPrimaryKey):
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
    )

    options = models.ManyToManyField(
        MenuOptions,
        related_name='options',
    )


class  EmployeesMenuAnswer(UUIDPrimaryKey):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='answers',
    )

    menu_option = models.ForeignKey(
        MenuOptions,
        on_delete=models.CASCADE,
        related_name='answers',
        blank=True,
        null=True,
    )

    employee_name = models.CharField(
        max_length=64,
        blank=True,
        null=True
    )

    comentaries = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )
