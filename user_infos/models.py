from django.db import models


class UserInfo(models.Model):
    email = models.EmailField(
        blank=True,
        null=True
    )
    telegram = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    instagram = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    phone = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Контакты пользователя"
        verbose_name_plural = "Контакты пользователей"

    def __str__(self) -> str:
        return f'{self.id}'
