from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    slug = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    todos_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} ({self.slug})'



class TodoItem(models.Model):

    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3

    priority_counts = {
        PRIORITY_HIGH: 0,
        PRIORITY_MEDIUM: 0,
        PRIORITY_LOW: 0,
    }

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "Высокий приоритет"),
        (PRIORITY_MEDIUM, "Средний приоритет"),
        (PRIORITY_LOW, "Низкий приоритет"),
    ]

    description = models.TextField("описание")
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="tasks"
    )
    priority = models.IntegerField(
        "Приоритет", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    category = models.ManyToManyField(Category, blank=True)
    was_priority = models.SmallIntegerField(default=0)


    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])


class PriorityCount(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=300)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.title, self.count)

    class Meta:
        verbose_name = 'Счетчик приоритетов'
        verbose_name_plural = 'Счетчик приоритетов'
