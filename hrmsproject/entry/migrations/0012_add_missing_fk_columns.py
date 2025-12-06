# Generated manually to add missing ForeignKey columns

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0011_remove_manualentry_shift_type_manualentry_shift_and_more'),
        ('master', '0021_add_shift_roster_models'),
    ]

    operations = [
        # Add salary_type_id column if it doesn't exist (without FK constraint first)
        migrations.RunSQL(
            """
            SET @exist := (SELECT COUNT(*) FROM information_schema.columns 
                          WHERE table_schema = DATABASE() 
                          AND table_name = 'entry_manualentry' 
                          AND column_name = 'salary_type_id');
            SET @sqlstmt := IF(@exist = 0, 
                'ALTER TABLE entry_manualentry ADD COLUMN salary_type_id INT NULL',
                'SELECT 1');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Add shift_id column if it doesn't exist (skip if already exists)
        migrations.RunSQL(
            """
            SET @exist := (SELECT COUNT(*) FROM information_schema.columns 
                          WHERE table_schema = DATABASE() 
                          AND table_name = 'entry_manualentry' 
                          AND column_name = 'shift_id');
            SET @sqlstmt := IF(@exist = 0, 
                'ALTER TABLE entry_manualentry ADD COLUMN shift_id INT NULL',
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Add leave_type_id column if it doesn't exist (without FK constraint first)
        migrations.RunSQL(
            """
            SET @exist := (SELECT COUNT(*) FROM information_schema.columns 
                          WHERE table_schema = DATABASE() 
                          AND table_name = 'entry_leaveentry' 
                          AND column_name = 'leave_type_id');
            SET @sqlstmt := IF(@exist = 0, 
                'ALTER TABLE entry_leaveentry ADD COLUMN leave_type_id INT NULL',
                'SELECT 1');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Now add the ForeignKey fields to Django's state (only if columns were added)
        migrations.AlterField(
            model_name='manualentry',
            name='salary_type',
            field=models.ForeignKey(blank=True, help_text='Salary type from master data', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manual_entries', to='master.salarytype'),
        ),
        migrations.AlterField(
            model_name='leaveentry',
            name='leave_type',
            field=models.ForeignKey(blank=True, help_text='Leave type from master data', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='leave_entries', to='master.leavetype'),
        ),
    ]
