# Generated by Django 3.2.8 on 2021-10-15 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usermatch',
            unique_together={('from_user', 'for_user')},
        ),
    ]