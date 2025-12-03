# Generated manually to add ShiftRoster models

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0020_add_document_to_expensetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftRoster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary_type', models.CharField(choices=[('SALARY', 'Salary'), ('WAGES', 'Wages'), ('OTHERS', 'Others')], max_length=20)),
                ('from_date', models.DateField()),
                ('to_date', models.DateField(blank=True, help_text='Optional end date for month rosters', null=True)),
                ('roster_type', models.CharField(choices=[('WEEK', 'Week Wise'), ('MONTH', 'Month Wise')], default='WEEK', max_length=10)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], default='Draft', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shift_rosters', to='master.site')),
            ],
            options={
                'verbose_name': 'Shift Roster',
                'verbose_name_plural': 'Shift Rosters',
                'ordering': ['-from_date', 'site__name'],
            },
        ),
        migrations.CreateModel(
            name='ShiftRosterAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('shift_name', models.CharField(blank=True, help_text='Shift name (e.g., DAY SHIFT, NIGHT SHIFT)', max_length=100)),
                ('is_day_off', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='roster_assignments', to='master.employee')),
                ('roster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='master.shiftroster')),
                ('shift', models.ForeignKey(blank=True, help_text='Optional: Link to Shift model', null=True, on_delete=django.db.models.deletion.PROTECT, to='master.shift')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='roster_site_assignments', to='master.site')),
            ],
            options={
                'verbose_name': 'Shift Roster Assignment',
                'verbose_name_plural': 'Shift Roster Assignments',
                'ordering': ['date', 'employee__staff_name'],
                'unique_together': {('roster', 'employee', 'date')},
            },
        ),
    ]

