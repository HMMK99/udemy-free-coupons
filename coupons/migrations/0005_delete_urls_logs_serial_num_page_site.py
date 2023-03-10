# Generated by Django 4.1.7 on 2023-02-27 03:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("coupons", "0004_urls_remove_logs_serial_num_remove_page_site"),
    ]

    operations = [
        migrations.DeleteModel(
            name="URLs",
        ),
        migrations.AddField(
            model_name="logs",
            name="serial_num",
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="page",
            name="site",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="coupons.website",
            ),
        ),
    ]
