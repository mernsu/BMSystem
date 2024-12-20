# Generated by Django 5.1.2 on 2024-11-20 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BMSystem", "0009_remove_book_published_year_book_published_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="myuser",
            name="groups",
        ),
        migrations.RemoveField(
            model_name="myuser",
            name="user_permissions",
        ),
        migrations.AddField(
            model_name="book",
            name="isbn",
            field=models.CharField(default="0000000000000", max_length=13, unique=True),
        ),
        migrations.DeleteModel(
            name="BorrowRecord",
        ),
        migrations.DeleteModel(
            name="MyUser",
        ),
    ]
