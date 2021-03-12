# Generated by Django 3.1.7 on 2021-03-12 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(related_query_name='posts', to='posts.Hashtags'),
        ),
    ]
