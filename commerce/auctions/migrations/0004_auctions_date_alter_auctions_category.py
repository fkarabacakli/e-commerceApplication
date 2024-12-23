# Generated by Django 4.2.4 on 2023-12-14 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "auctions",
            "0003_auctions_description_auctions_image_auctions_price_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="auctions",
            name="date",
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="auctions",
            name="category",
            field=models.CharField(
                choices=[
                    ("MDA", "Media"),
                    ("BVR", "Beverages"),
                    ("FSH", "Fashion"),
                    ("ELC", "Electronics"),
                    ("FOD", "Food"),
                    ("FNT", "Furniture"),
                ],
                default="FSH",
                max_length=3,
            ),
        ),
    ]
