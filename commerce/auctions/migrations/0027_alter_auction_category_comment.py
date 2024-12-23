# Generated by Django 4.2.4 on 2024-01-18 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0026_alter_auction_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="category",
            field=models.CharField(
                choices=[
                    ("FSH", "Fashion"),
                    ("MDA", "Media"),
                    ("FOD", "Food"),
                    ("ELC", "Electronics"),
                    ("FNT", "Furniture"),
                    ("BVR", "Beverages"),
                ],
                default="FSH",
                max_length=3,
            ),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("comment_text", models.TextField()),
                ("comment_date", models.DateField(auto_now=True)),
                (
                    "comment_product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_product",
                        to="auctions.auction",
                    ),
                ),
                (
                    "comment_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]