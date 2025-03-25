from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_plated_end_at'),
    ]

    operations = [
        # Преобразование поля created_at
        migrations.RunSQL(
            sql="""
                ALTER TABLE order_order 
                ALTER COLUMN created_at 
                TYPE timestamp with time zone 
                USING to_timestamp(created_at::double precision);
            """,
            reverse_sql="""
                ALTER TABLE order_order 
                ALTER COLUMN created_at 
                TYPE integer 
                USING EXTRACT(epoch FROM created_at)::integer;
            """,
        ),
        # Преобразование поля end_at
        migrations.RunSQL(
            sql="""
                ALTER TABLE order_order 
                ALTER COLUMN end_at 
                TYPE timestamp with time zone 
                USING to_timestamp(end_at::double precision);
            """,
            reverse_sql="""
                ALTER TABLE order_order 
                ALTER COLUMN end_at 
                TYPE integer 
                USING EXTRACT(epoch FROM end_at)::integer;
            """,
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='end_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='plated_end_at',
            field=models.DateTimeField(),
        ),
    ]