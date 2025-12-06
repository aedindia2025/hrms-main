# Generated manually to verify and fix columns - final attempt

from django.db import migrations


def verify_and_fix_columns(apps, schema_editor):
    """
    Verify column state and fix if needed using raw SQL.
    """
    with schema_editor.connection.cursor() as cursor:
        # Check leave_type_id column
        cursor.execute("""
            SELECT COLUMN_NAME, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'entry_leaveentry'
            AND COLUMN_NAME = 'leave_type_id'
        """)
        result = cursor.fetchone()
        if result:
            column_name, is_nullable, column_default, column_type = result
            print(f"leave_type_id: nullable={is_nullable}, default={column_default}, type={column_type}")
            
            # If not nullable, make it nullable
            if is_nullable == 'NO':
                print("Making leave_type_id nullable...")
                cursor.execute("ALTER TABLE entry_leaveentry MODIFY COLUMN leave_type_id INT NULL")
        
        # Check salary_type_id column
        cursor.execute("""
            SELECT COLUMN_NAME, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'entry_manualentry'
            AND COLUMN_NAME = 'salary_type_id'
        """)
        result = cursor.fetchone()
        if result:
            column_name, is_nullable, column_default, column_type = result
            print(f"salary_type_id: nullable={is_nullable}, default={column_default}, type={column_type}")
            
            if is_nullable == 'NO':
                print("Making salary_type_id nullable...")
                cursor.execute("ALTER TABLE entry_manualentry MODIFY COLUMN salary_type_id INT NULL")
        
        # Check shift_id column
        cursor.execute("""
            SELECT COLUMN_NAME, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_TYPE
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = DATABASE()
            AND TABLE_NAME = 'entry_manualentry'
            AND COLUMN_NAME = 'shift_id'
        """)
        result = cursor.fetchone()
        if result:
            column_name, is_nullable, column_default, column_type = result
            print(f"shift_id: nullable={is_nullable}, default={column_default}, type={column_type}")
            
            if is_nullable == 'NO':
                print("Making shift_id nullable...")
                cursor.execute("ALTER TABLE entry_manualentry MODIFY COLUMN shift_id INT NULL")


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0015_direct_fix_nullable'),
    ]

    operations = [
        migrations.RunPython(verify_and_fix_columns, reverse_code=migrations.RunPython.noop),
    ]

