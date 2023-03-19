# Generated by Django 4.1.2 on 2023-03-13 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lojas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=64)),
                ('apikey', models.CharField(max_length=11)),
                ('apisecret', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Emprestimos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('status', models.CharField(choices=[('PAGO', 'Ja foi pago'), ('DEVENDO', 'Nao foi pago')], max_length=20)),
                ('credor', models.ManyToManyField(related_name='credor', to='omieemprestimos.lojas')),
                ('devedor', models.ManyToManyField(related_name='devedor', to='omieemprestimos.lojas')),
            ],
        ),
    ]
