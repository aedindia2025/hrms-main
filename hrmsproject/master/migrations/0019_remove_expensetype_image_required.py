# Generated manually to remove image_required field from ExpenseType

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0018_alter_employeeassetassignment_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expensetype',
            name='image_required',
        ),
    ]

