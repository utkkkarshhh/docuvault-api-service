import os
from django.db.backends.signals import connection_created
from django.dispatch import receiver
from django.conf import settings

# Added specifically for Neon
@receiver(connection_created)
def set_search_path(sender, connection, **kwargs):
    if connection.vendor != 'postgresql':
        return

    schema_name = 'public'
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO public, public")
