# Generated manually to remove old salary_type column

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0017_remove_old_leave_type_column'),
    ]

    operations = [
        # Remove old salary_type varchar column if it exists
        migrations.RunSQL(
            """
            SET @exist := (SELECT COUNT(*) FROM information_schema.columns 
                          WHERE table_schema = DATABASE() 
                          AND table_name = 'entry_manualentry' 
                          AND column_name = 'salary_type'
                          AND column_type LIKE 'varchar%');
            SET @sqlstmt := IF(@exist > 0, 
                'ALTER TABLE entry_manualentry DROP COLUMN salary_type',
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
