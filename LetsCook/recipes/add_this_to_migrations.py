"""
from django.contrib.postgres.operations import HStoreExtension

class Migration(migrations.Migration):
    ...

    operations = [
        HStoreExtension(),
        ...
    ]
"""