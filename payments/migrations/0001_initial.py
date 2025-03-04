# Generated by Django 5.1.6 on 2025-03-04 11:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('credits', '0001_initial'),
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField()),
                ('credit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='credits.credit')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary.dictionary')),
            ],
        ),
    ]
