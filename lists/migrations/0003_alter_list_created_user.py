# Generated by Django 4.0 on 2022-02-25 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
        ('lists', '0002_remove_comment_list_comment_comment_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='created_user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='auctions.user'),
        ),
    ]