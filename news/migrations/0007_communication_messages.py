# Generated by Django 2.2.4 on 2019-08-07 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_mailinglist_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='communication',
            name='messages',
            field=models.ManyToManyField(to='news.Message'),
        ),
    ]