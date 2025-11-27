from django.db import models


class SiteEntry(models.Model):
    TRANSFER_TYPE_MONTH = 'Month'
    TRANSFER_TYPE_WEEK = 'Week'
    TRANSFER_TYPE_CHOICES = [
        (TRANSFER_TYPE_MONTH, 'Month'),
        (TRANSFER_TYPE_WEEK, 'Week'),
    ]

    transfer_date = models.DateField()
    employee_name = models.CharField(max_length=255)
    from_site = models.CharField(max_length=255)
    to_site = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    transfer_type = models.CharField(
        max_length=10,
        choices=TRANSFER_TYPE_CHOICES,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-transfer_date', 'employee_name']
        verbose_name = 'Site Transfer Entry'
        verbose_name_plural = 'Site Transfer Entries'

    def __str__(self):
        return f'{self.employee_name} - {self.transfer_date}'
