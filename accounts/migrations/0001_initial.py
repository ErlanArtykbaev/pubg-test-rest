

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=30, unique=True, verbose_name='Phone')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='Name')),
                ('contact_number', models.CharField(blank=True, max_length=100, verbose_name='Contact Number')),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=14, verbose_name='Name')),
                ('activation_code', models.CharField(blank=True, max_length=6, verbose_name='Activation Code')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Date joined')),
                ('player_id', models.CharField(max_length=255, unique=True, blank=True)),


                ('link_code', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
    ]
