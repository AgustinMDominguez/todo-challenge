# Generated by Django 3.2.6 on 2021-08-30 14:52

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('todo', '0002_alter_profile_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, max_length=1000, null=True)),
                ('done', models.BooleanField(default=False)),
                ('favorite', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.task')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.profile')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
