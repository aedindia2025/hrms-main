from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0017_employee_employeevehicledetail_employeequalification_and_more'),
        ('entry', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompOffEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField()),
                ('in_time', models.TimeField()),
                ('out_time', models.TimeField()),
                ('worked_duration', models.DurationField(blank=True, help_text='Stores total worked duration for the day.', null=True)),
                ('day_status', models.CharField(choices=[('full_day', 'Full Day'), ('half_day', 'Half Day'), ('overtime', 'Overtime')], max_length=20)),
                ('head_approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('head_approval_by', models.CharField(blank=True, max_length=255)),
                ('head_approval_note', models.CharField(blank=True, max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comp_off_entries', to='master.employee')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comp_off_entries', to='master.site')),
            ],
            options={
                'verbose_name': 'Comp-Off Entry',
                'verbose_name_plural': 'Comp-Off Entries',
                'ordering': ['-work_date', 'employee__staff_name'],
            },
        ),
    ]

