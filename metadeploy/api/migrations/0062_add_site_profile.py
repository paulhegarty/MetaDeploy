# Generated by Django 2.1.7 on 2019-03-13 01:05

import django.db.models.deletion
import parler.models
import sfdo_template_helpers.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        ("api", "0061_no_null_product_on_plantemplate"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteProfile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("logo", models.ImageField(blank=True, upload_to="")),
                (
                    "site",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.Site"
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="SiteProfileTranslation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "language_code",
                    models.CharField(
                        db_index=True, max_length=15, verbose_name="Language"
                    ),
                ),
                ("name", models.CharField(max_length=64)),
                (
                    "welcome_text",
                    sfdo_template_helpers.fields.MarkdownField(
                        blank=True, property_suffix="_markdown"
                    ),
                ),
                (
                    "copyright_notice",
                    sfdo_template_helpers.fields.MarkdownField(
                        blank=True, property_suffix="_markdown"
                    ),
                ),
                (
                    "master",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="translations",
                        to="api.SiteProfile",
                    ),
                ),
            ],
            options={
                "verbose_name": "site profile Translation",
                "db_table": "api_siteprofile_translation",
                "db_tablespace": "",
                "managed": True,
                "default_permissions": (),
            },
        ),
        migrations.AlterUniqueTogether(
            name="siteprofiletranslation", unique_together={("language_code", "master")}
        ),
    ]
