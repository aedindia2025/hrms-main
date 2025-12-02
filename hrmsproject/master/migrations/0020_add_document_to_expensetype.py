# Generated manually to add document field to ExpenseType

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0019_remove_expensetype_image_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='expensetype',
            name='document',
            field=models.FileField(blank=True, help_text='Upload document related to this expense type', null=True, upload_to='expense_type/documents/'),
        ),
    ]

