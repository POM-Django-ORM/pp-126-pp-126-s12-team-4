from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE order_order 
                ALTER COLUMN plated_end_at 
                TYPE timestamp with time zone 
                USING to_timestamp(plated_end_at);
            """,
            reverse_sql="""
                ALTER TABLE order_order 
                ALTER COLUMN plated_end_at 
                TYPE integer 
                USING EXTRACT(epoch FROM plated_end_at)::integer;
            """,
        ),
    ]