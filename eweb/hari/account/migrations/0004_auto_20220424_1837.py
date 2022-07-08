# Generated by Django 3.2.5 on 2022-04-24 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20220424_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentcart',
            name='status',
        ),
        migrations.AddField(
            model_name='ordereditems',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('OUT FOR DELIVERY', 'OUT FOR DELIVERY'), ('DELIVERED', 'DELIVERED')], default='PENDING', max_length=200),
        ),
    ]