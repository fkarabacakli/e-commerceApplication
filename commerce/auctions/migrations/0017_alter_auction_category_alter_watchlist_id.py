# Generated by Django 4.2.4 on 2024-01-16 05:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0016_alter_auction_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="category",
            field=models.CharField(
                choices=[
                    ("FOD", "Food"),
                    ("BVR", "Beverages"),
                    ("FSH", "Fashion"),
                    ("FNT", "Furniture"),
                    ("ELC", "Electronics"),
                    ("MDA", "Media"),
                ],
                default="FSH",
                max_length=3,
            ),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
