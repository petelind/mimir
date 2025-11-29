# Generated migration to rename Activity.description to Activity.guidance

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('methodology', '0004_remove_activity_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='description',
            new_name='guidance',
        ),
    ]
