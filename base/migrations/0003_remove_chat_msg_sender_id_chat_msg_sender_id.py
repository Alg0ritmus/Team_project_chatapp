# Generated by Django 4.0 on 2022-11-20 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_chat_msg_sender_id_chat_msg_sender_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat_msg',
            name='sender_id',
        ),
        migrations.AddField(
            model_name='chat_msg',
            name='sender_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.chat_user'),
            preserve_default=False,
        ),
    ]
