# Generated manually to remove old leave_type column

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0016_verify_and_fix_columns'),
    ]

    operations = [
        # Remove old leave_type varchar column
        migrations.RunSQL(
            """
            SET @exist := (SELECT COUNT(*) FROM information_schema.columns 
                          WHERE table_schema = DATABASE() 
                          AND table_name = 'entry_leaveentry' 
                          AND column_name = 'leave_type'
                          AND column_type LIKE 'varchar%');
            SET @sqlstmt := IF(@exist > 0, 
                'ALTER TABLE entry_leaveentry DROP COLUMN leave_type',
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

