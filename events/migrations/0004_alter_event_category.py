# Generated by Django 5.2.2 on 2025-06-20 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_registration_event_alter_registration_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(choices=[('tecnologia', 'Técnologia'), ('educacao', 'Educação'), ('saude', 'Saúde'), ('empreendedorismo', 'Empreendedorismo')], max_length=20),
        ),
    ]
