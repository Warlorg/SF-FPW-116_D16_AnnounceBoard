# Generated by Django 4.2.4 on 2023-09-03 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercomment',
            old_name='announce',
            new_name='reaction',
        ),
        migrations.AlterField(
            model_name='announce',
            name='upload',
            field=models.FileField(blank=True, upload_to='uploads/'),
        ),
    ]
