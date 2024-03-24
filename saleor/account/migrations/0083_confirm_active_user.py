# Generated by Django 3.2.24 on 2024-02-29 13:21

from django.db import migrations
from django.db.models import QuerySet

# Batch size of 5000 is about ~8MB of memory usage
BATCH_SIZE = 5000


def queryset_in_batches(queryset):
    """Slice a queryset into batches.

    Input queryset should be sorted be pk.
    """
    start_pk = 0

    while True:
        qs = queryset.filter(pk__gt=start_pk)[:BATCH_SIZE]
        pks = list(qs.values_list("pk", flat=True))

        if not pks:
            break

        yield pks

        start_pk = pks[-1]


def set_user_is_confirmed_to_true(qs: QuerySet):
    qs.update(is_confirmed=True)


def confirm_active_users(apps, schema_editor):
    User = apps.get_model("account", "User")

    users = User.objects.order_by("pk").filter(
        is_confirmed=False, is_active=True, last_login__isnull=False
    )
    for ids in queryset_in_batches(users):
        qs = User.objects.filter(pk__in=ids)
        set_user_is_confirmed_to_true(qs)


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0082_auto_20231204_1419"),
    ]

    operations = [migrations.RunPython(confirm_active_users, migrations.RunPython.noop)]
