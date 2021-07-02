# Generated by Django 3.0.3 on 2020-08-08 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docname', models.CharField(max_length=40)),
                ('datecreate', models.DateTimeField(auto_now_add=True)),
                ('datelast', models.DateTimeField(auto_now=True)),
                ('setname', models.CharField(blank=True, max_length=100)),
                ('typename', models.CharField(max_length=10)),
                ('keywords', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ('-datecreate',),
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.CharField(max_length=1000)),
                ('datecreate', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Prefers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefer', models.PositiveIntegerField()),
                ('explore', models.PositiveIntegerField()),
                ('article', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.TextField(max_length=30)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('typename', models.TextField(max_length=10)),
                ('introduction', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=30)),
                ('html', models.TextField(max_length=30)),
                ('introduction', models.TextField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ZoneDiary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('img', models.TextField(null=True)),
            ],
            options={
                'ordering': ('-time',),
            },
        ),
    ]
