# Generated by Django 4.1.1 on 2022-09-20 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myprofile", "0002_auto_20220905_1730"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="myprofile",
            options={"permissions": (("can_change_myprofile", "can change profile"),)},
        ),
    ]
