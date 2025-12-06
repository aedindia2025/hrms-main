# Generated manually to directly fix nullable columns

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0014_force_nullable_columns'),
    ]

    operations = [
        # Direct SQL to make leave_type_id nullable - no FK constraints
        migrations.RunSQL(
            """
            ALTER TABLE entry_leaveentry MODIFY COLUMN leave_type_id INT NULL DEFAULT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Direct SQL to make salary_type_id nullable
        migrations.RunSQL(
            """
            ALTER TABLE entry_manualentry MODIFY COLUMN salary_type_id INT NULL DEFAULT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
        # Direct SQL to make shift_id nullable
        migrations.RunSQL(
            """
            ALTER TABLE entry_manualentry MODIFY COLUMN shift_id INT NULL DEFAULT NULL;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

