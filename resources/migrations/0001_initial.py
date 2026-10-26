                                               

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('books', 'Books'), ('notes', 'Notes'), ('equipment', 'Equipment'), ('previous_questions', 'Previous Questions'), ('course_materials', 'Course Materials')], max_length=30)),
                ('description', models.TextField(blank=True)),
                ('author', models.CharField(blank=True, max_length=150)),
                ('department', models.CharField(blank=True, max_length=100)),
                ('course_code', models.CharField(blank=True, max_length=50)),
                ('share_type', models.CharField(choices=[('share', 'Share'), ('rent', 'Rent'), ('sell', 'Sell')], default='share', max_length=20)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=30, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='resources/')),
                ('image', models.ImageField(blank=True, null=True, upload_to='resource_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resource_items', to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='ResourceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='resources.resourceitem')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_reviews', to='accounts.student')),
            ],
        ),
    ]
