# Generated by Django 2.2.10 on 2020-04-25 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('majora2', '0057_publishedartifactgroup_is_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='PAGQualityReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass', models.BooleanField(default=False)),
                ('test_set_ruleset', models.CharField(max_length=64)),
                ('test_set_version', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryMajoraArtifactMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.AddField(
            model_name='majoraartifact',
            name='is_pagged',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='TemporaryMajoraArtifactMetric_Dehum',
            fields=[
                ('temporarymajoraartifactmetric_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='majora2.TemporaryMajoraArtifactMetric')),
                ('total_dropped', models.PositiveIntegerField()),
                ('n_hits', models.PositiveIntegerField()),
                ('n_clipped', models.PositiveIntegerField()),
                ('n_known', models.PositiveIntegerField()),
                ('n_collateral', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('majora2.temporarymajoraartifactmetric',),
        ),
        migrations.CreateModel(
            name='TemporaryMajoraArtifactMetric_Mapping',
            fields=[
                ('temporarymajoraartifactmetric_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='majora2.TemporaryMajoraArtifactMetric')),
                ('num_pos', models.PositiveIntegerField()),
                ('num_maps', models.PositiveIntegerField(blank=True, null=True)),
                ('num_unmaps', models.PositiveIntegerField(blank=True, null=True)),
                ('median_cov', models.FloatField(blank=True, null=True)),
                ('mean_cov', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte1', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte5', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte10', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte20', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte50', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte100', models.FloatField(blank=True, null=True)),
                ('pc_pos_cov_gte200', models.FloatField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('majora2.temporarymajoraartifactmetric',),
        ),
        migrations.CreateModel(
            name='TemporaryMajoraArtifactMetric_Mapping_Tiles',
            fields=[
                ('temporarymajoraartifactmetric_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='majora2.TemporaryMajoraArtifactMetric')),
                ('n_tiles', models.PositiveSmallIntegerField()),
                ('pc_tiles_meancov_gte1', models.FloatField()),
                ('pc_tiles_meancov_gte5', models.FloatField()),
                ('pc_tiles_meancov_gte10', models.FloatField()),
                ('pc_tiles_meancov_gte20', models.FloatField()),
                ('pc_tiles_meancov_gte50', models.FloatField()),
                ('pc_tiles_meancov_gte100', models.FloatField()),
                ('pc_tiles_meancov_gte200', models.FloatField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('majora2.temporarymajoraartifactmetric',),
        ),
        migrations.CreateModel(
            name='TemporaryMajoraArtifactMetric_Sequence',
            fields=[
                ('temporarymajoraartifactmetric_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='majora2.TemporaryMajoraArtifactMetric')),
                ('num_seqs', models.PositiveIntegerField()),
                ('num_bases', models.PositiveIntegerField()),
                ('pc_acgt', models.PositiveIntegerField()),
                ('pc_masked', models.PositiveIntegerField()),
                ('pc_invalid', models.PositiveIntegerField()),
                ('longest_gap', models.PositiveIntegerField(blank=True, null=True)),
                ('longest_ungap', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('majora2.temporarymajoraartifactmetric',),
        ),
        migrations.AddField(
            model_name='temporarymajoraartifactmetric',
            name='artifact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='majora2.MajoraArtifact'),
        ),
        migrations.AddField(
            model_name='temporarymajoraartifactmetric',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_majora2.temporarymajoraartifactmetric_set+', to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='PAGQualityReportRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass', models.BooleanField(default=False)),
                ('is_warn', models.BooleanField(default=False)),
                ('test_name', models.CharField(max_length=64)),
                ('test_desc', models.CharField(max_length=128)),
                ('test_value_s', models.CharField(blank=True, max_length=64, null=True)),
                ('test_value_f', models.FloatField(blank=True, null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reports', to='majora2.PAGQualityReport')),
            ],
        ),
        migrations.CreateModel(
            name='PAGQualityReportGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass', models.BooleanField(default=False)),
                ('test_set_name', models.CharField(max_length=64)),
                ('pag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='quality_tests', to='majora2.PublishedArtifactGroup')),
            ],
        ),
        migrations.AddField(
            model_name='pagqualityreport',
            name='report_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reports', to='majora2.PAGQualityReportGroup'),
        ),
    ]
