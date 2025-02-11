# Generated by Django 5.0.2 on 2024-02-23 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BugData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug_title', models.CharField(max_length=200)),
                ('bug_detail', models.TextField()),
                ('deadline_time', models.CharField(max_length=20)),
                ('submitted_time', models.CharField(max_length=20)),
                ('bug_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bug_from_user', to='home.userdetail')),
                ('bug_reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bug_reviewer_user', to='home.userdetail')),
                ('bug_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bug_to_user', to='home.userdetail')),
            ],
        ),
        migrations.CreateModel(
            name='BugReviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=20)),
                ('dAndTime', models.CharField(max_length=20)),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.bugdata')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_u_n', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('project_description', models.TextField()),
                ('project_created_time', models.CharField(max_length=20)),
                ('project_gtihub_link', models.TextField()),
                ('project_phase', models.CharField(max_length=20)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.userdetail')),
            ],
        ),
        migrations.CreateModel(
            name='LlmData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_asked', models.TextField()),
                ('answer_from_api', models.TextField()),
                ('time_of_message', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.userdetail')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
            ],
        ),
        migrations.CreateModel(
            name='ChatData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField()),
                ('time_of_message', models.CharField(max_length=20)),
                ('msg_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.userdetail')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement_msg', models.CharField(max_length=200)),
                ('time_of_message', models.CharField(max_length=20)),
                ('ann_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ann_from_user', to='home.userdetail')),
                ('ann_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ann_to_user', to='home.userdetail')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFunctionalities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_funcionalities', models.CharField(max_length=200)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.userdetail')),
            ],
        ),
        migrations.CreateModel(
            name='ReportBug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug_by_detail', models.TextField()),
                ('bug_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.userdetail')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
            ],
        ),
        migrations.AddField(
            model_name='bugdata',
            name='bug_reported_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.reportbug'),
        ),
        migrations.CreateModel(
            name='SprintData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sprint_title', models.CharField(max_length=200)),
                ('sprint_detail', models.TextField()),
                ('deadline_time', models.CharField(max_length=20)),
                ('submitted_time', models.CharField(max_length=20)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.projectdetail')),
                ('sprint_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprint_from_user', to='home.userdetail')),
                ('sprint_reviewer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sprint_reviewer_user', to='home.userdetail')),
                ('sprint_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprint_to_user', to='home.userdetail')),
            ],
        ),
        migrations.CreateModel(
            name='SprintReviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(max_length=20)),
                ('dAndTime', models.CharField(max_length=20)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.sprintdata')),
            ],
        ),
    ]
