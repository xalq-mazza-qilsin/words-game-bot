# Generated by Django 4.2.3 on 2023-07-28 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_guessedletter'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='game',
            unique_together={('user', 'word')},
        ),
    ]
