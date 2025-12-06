# Generated manually to force columns to be nullable

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0013_fix_leave_type_nullable'),
    ]

    operations = [
        # Force leave_type_id to be nullable - drop FK, modify (don't add FK back, Django handles it)
        migrations.RunSQL(
            """
            -- Drop foreign key constraint if exists
            SET @fk_name := (SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'entry_leaveentry' 
                            AND COLUMN_NAME = 'leave_type_id' 
                            AND REFERENCED_TABLE_NAME IS NOT NULL 
                            LIMIT 1);
            SET @sqlstmt := IF(@fk_name IS NOT NULL AND @fk_name != '', 
                CONCAT('ALTER TABLE entry_leaveentry DROP FOREIGN KEY ', @fk_name),
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            
            -- Modify column to be nullable
            ALTER TABLE entry_leaveentry MODIFY COLUMN leave_type_id INT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Force salary_type_id to be nullable
        migrations.RunSQL(
            """
            SET @fk_name := (SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'entry_manualentry' 
                            AND COLUMN_NAME = 'salary_type_id' 
                            AND REFERENCED_TABLE_NAME IS NOT NULL 
                            LIMIT 1);
            SET @sqlstmt := IF(@fk_name IS NOT NULL AND @fk_name != '', 
                CONCAT('ALTER TABLE entry_manualentry DROP FOREIGN KEY ', @fk_name),
                'SELECT 1 as skip');
            PREPARE stmt FROM @sqlstmt;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            
            ALTER TABLE entry_manualentry MODIFY COLUMN salary_type_id INT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Force shift_id to be nullable
        migrations.RunSQL(
            """
            SET @fk_name := (SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
                            WHERE TABLE_SCHEMA = DATABASE() 
                            AND TABLE_NAME = 'entry_manualentry' 
                            AND COLUMN_NAME = 'shift_id' 
                            AND REFERENCED_TABLE_NAME IS NOT NULL 
                            LIMIT 1);
            SET @sqlstmt := IF(@fk_name IS NOT NULL AND @fk_name != '', 
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

