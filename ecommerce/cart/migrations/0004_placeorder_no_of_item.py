# Generated by Django 5.0.1 on 2024-02-05 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_alter_placeorder_product_alter_placeorder_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeorder',
            name='no_of_item',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
