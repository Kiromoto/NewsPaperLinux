# Generated by Django 4.0.5 on 2022-08-10 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_categorysubscriber_category_subscriber_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='categorysubscriber',
            old_name='subscriber_us',
            new_name='subscriber_user',
        ),
    ]
