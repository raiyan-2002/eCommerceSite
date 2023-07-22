# Generated by Django 4.2.3 on 2023-07-21 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0006_listing_active_listing_watchers"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="winner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="winner1",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="listing",
            name="watchers",
            field=models.ManyToManyField(
                blank=True, related_name="watchlisters", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]