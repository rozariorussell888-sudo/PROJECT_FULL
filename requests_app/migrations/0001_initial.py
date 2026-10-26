                                               

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResourceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('books', 'Books'), ('notes', 'Notes'), ('equipment', 'Equipment'), ('previous_questions', 'Previous Questions'), ('course_materials', 'Course Materials')], max_length=30)),
                ('course_code', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resource_requests', to='accounts.student')),
            ],
        ),
        migrations.CreateModel(
            name='ProductRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_product_requests', to='accounts.student')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_requests', to='resources.resourceitem')),
            ],
            options={
                'ordering': ['-created_at'],
                'constraints': [models.UniqueConstraint(fields=('resource', 'requester'), name='unique_resource_requester')],
            },
        ),
    ]
