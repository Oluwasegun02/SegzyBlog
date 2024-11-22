# Example migration file (e.g., 0002_auto_20210906_1234.py)
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default='default-slug', max_length=200, unique=True),
            preserve_default=False,
        ),
        # other operations...
    ]
