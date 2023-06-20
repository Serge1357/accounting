# Generated by Django 4.2 on 2023-05-21 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_transaction_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='expense_category',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='category',
            name='income_category',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
