from django.db import migrations
from django.contrib.auth.hashers import make_password

group_1_name = 'vendedores'
group_2_name = 'conferentes'


def create_default_environment(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    environment = apps.get_model('portal', 'Environment')
    environment.objects.using(db_alias).bulk_create([
        environment(name="Campinas"),
        environment(name="Brasília"),
        environment(name="Ribeirão Preto")
    ])


def create_sample_groups(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    group = apps.get_model('auth', 'Group')
    group.objects.using(db_alias).bulk_create([
        group(name=group_1_name),
        group(name=group_2_name)
    ])


def create_sample_employees(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    employee = apps.get_model('portal', 'Employee')
    employee.objects.using(db_alias).bulk_create([
        employee(user=apps.get_model('auth', 'User').objects.create(
                username='leonardo',
                password=make_password("abc123"),
                first_name='Leonardo',
                last_name='Romanini',
                is_superuser=True,
                is_staff=True),
                environment_id=1),
        employee(user=apps.get_model('auth', 'User').objects.create(
            username='drauzio',
            password=make_password("abc123"),
            first_name='Drauzio',
            last_name='Varella',
            is_superuser=True,
            is_staff=True),
            environment_id=1),
        employee(user_id=1, environment_id=2),
        employee(user_id=2, environment_id=2),
        employee(user_id=1, environment_id=3),
        employee(user_id=2, environment_id=3)
    ])


def add_employees_to_groups(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    group = apps.get_model('auth', 'Group')
    user = apps.get_model('auth', 'User')
    group_1 = group.objects.using(db_alias).get(name=group_1_name)
    group_2 = group.objects.using(db_alias).get(name=group_2_name)

    group_1.user_set.add(user.objects.using(db_alias).get(id=1),
                         user.objects.using(db_alias).get(id=2))
    group_2.user_set.add(user.objects.using(db_alias).get(id=1),
                         user.objects.using(db_alias).get(id=2))


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_environment),
        migrations.RunPython(create_sample_employees),
        migrations.RunPython(create_sample_groups),
        migrations.RunPython(add_employees_to_groups)
    ]
