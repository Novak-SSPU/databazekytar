# Generated by Django 3.1.7 on 2021-06-21 17:37

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import guitars.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guitar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('stringnumber', models.IntegerField(blank=True, help_text='Please enter the number of strings', null=True, verbose_name='String number')),
                ('image', models.ImageField(blank=True, null=True, upload_to='guitar/images/%Y/%m/%d/', verbose_name='Image')),
                ('rate', models.FloatField(default=5.0, help_text='Please enter an float value (range 1.0 - 10.0)', null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(10.0)], verbose_name='Rate')),
                ('type', models.CharField(help_text='Select a type for this guitar', max_length=30, verbose_name=guitars.models.Type)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-rate', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter type of guitar', max_length=50, unique=True, verbose_name='Type name')),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('rate', models.IntegerField(default=5, help_text='Please enter an integer value (range 1 - 10)', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Rate')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('guitar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guitars.guitar')),
            ],
            options={
                'order_with_respect_to': 'guitar',
            },
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(null=True, upload_to=guitars.models.attachment_path, verbose_name='File')),
                ('type', models.CharField(blank=True, choices=[('audio', 'Audio'), ('image', 'Image'), ('text', 'Text'), ('video', 'Video'), ('other', 'Other')], default='image', help_text='Select allowed attachment type', max_length=5, verbose_name='Attachment type')),
                ('guitar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guitars.guitar')),
            ],
            options={
                'order_with_respect_to': 'guitar',
            },
        ),
    ]
