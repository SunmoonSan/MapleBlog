# Generated by Django 2.0.4 on 2018-05-15 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0002_auto_20180503_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuth_ex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(default='', max_length=64)),
                ('account', models.ForeignKey(on_delete=True, to='blog.Account')),
            ],
        ),
        migrations.CreateModel(
            name='OAuth_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=12)),
                ('title', models.CharField(max_length=12)),
                ('img', models.FileField(upload_to='static/img/connect')),
            ],
        ),
        migrations.AddField(
            model_name='oauth_ex',
            name='oauth_type',
            field=models.ForeignKey(default=1, on_delete=True, to='oauth.OAuth_type'),
        ),
    ]
