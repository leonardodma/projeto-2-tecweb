# Generated by Django 3.2 on 2021-05-04 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0002_rename_potcode_adoption_postcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adoption',
            name='adress',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='age',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='breed_primary',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='breed_secondary',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='city',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='gender',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='name',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='phone',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='postcode',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='size',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='state',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='adoption',
            name='status',
            field=models.CharField(default='Não encontrado', max_length=100),
        ),
        migrations.AlterField(
            model_name='dogs',
            name='img_url',
            field=models.CharField(max_length=100),
        ),
    ]
