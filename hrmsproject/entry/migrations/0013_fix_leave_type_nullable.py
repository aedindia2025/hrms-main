# Generated manually to fix leave_type column to allow NULL

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0012_add_missing_fk_columns'),
    ]

    operations = [
        # Make leave_type_id nullable - drop FK constraint first, modify, then add back
        migrations.RunSQL(
            """
            SET @fk_name := (SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'entry_leaveentry' 
                            AND COLUMN_NAME = 'leave_type_id' 
                            AND REFERENCED_TABLE_NAME IS NOT NULL 
                            LIMIT 1);
            SET @sqlstmt := IF(@fk_name IS NOT NULL, 
                CONCAT('ALTER TABLE entry_leaveentry DROP FOREIGN KEY ', @fk_name),
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            ALTER TABLE entry_leaveentry MODIFY COLUMN leave_type_id INT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Make salary_type_id nullable - drop FK constraint first, modify, then add back
        migrations.RunSQL(
            """
            SET @fk_name := (SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'entry_manualentry' 
                            AND COLUMN_NAME = 'salary_type_id' 
                            AND REFERENCED_TABLE_NAME IS NOT NULL 
                            LIMIT 1);
            SET @sqlstmt := IF(@fk_name IS NOT NULL, 
                CONCAT('ALTER TABLE entry_manualentry DROP FOREIGN KEY ', @fk_name),
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            ALTER TABLE entry_manualentry MODIFY COLUMN salary_type_id INT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Make shift_id nullable - drop FK constraint first, modify, then add back
        migrations.RunSQL(
            """
            SET @fk_name := (SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'entry_manualentry' 
                            AND COLUMN_NAME = 'shift_id' 
                            AND REFERENCED_TABLE_NAME IS NOT NULL 
                            LIMIT 1);
            SET @sqlstmt := IF(@fk_name IS NOT NULL, 
                CONCAT('ALTER TABLE entry_manualentry DROP FOREIGN KEY ', @fk_name),
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            ALTER TABLE entry_manualentry MODIFY COLUMN shift_id INT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
