# Generated by Django 5.1.2 on 2024-12-16 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BMSystem", "0017_borrowrecord_due_date_alter_borrowrecord_book_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowrecord",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
