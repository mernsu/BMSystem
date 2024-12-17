# Generated by Django 5.1.2 on 2024-12-04 12:23

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("BMSystem", "0011_alter_book_isbn"),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrower",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "borrower_id",
                    models.CharField(help_text="身份证号", max_length=100, unique=True),
                ),
                ("full_name", models.CharField(help_text="姓名", max_length=255)),
                (
                    "email",
                    models.EmailField(blank=True, help_text="邮箱地址", max_length=254),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, help_text="电话号码", max_length=20),
                ),
                (
                    "registration_date",
                    models.DateField(auto_now_add=True, help_text="借阅日期"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("booking_date", models.DateField(default=datetime.date.today)),
                ("due_date", models.DateField()),
                ("return_date", models.DateField(blank=True, null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="BMSystem.book",
                    ),
                ),
                (
                    "borrower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bookings",
                        to="BMSystem.borrower",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Bookings",
            },
        ),
    ]