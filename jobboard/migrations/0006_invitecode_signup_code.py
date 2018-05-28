# Generated by Django 2.0.3 on 2018-04-19 20:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170416_1821'),
        ('jobboard', '0005_auto_20180419_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitecode',
            name='signup_code',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.SignupCode'),
            preserve_default=False,
        ),
    ]