# Generated by Django 2.2.7 on 2019-12-09 01:06

import django.core.validators
import django.db.models.deletion
import mptt.fields
from django.conf import settings
from django.db import migrations, models

import django_ledger.models.mixins.io


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Account Code')),
                ('name', models.CharField(max_length=100, verbose_name='Account Name')),
                ('role', models.CharField(choices=[('Assets', (('ca', 'Current Asset'), ('lti', 'Long Term Investments'), ('ppe', 'Property Plant & Equipment'), ('ia', 'Intangible Assets'), ('aadj', 'Asset Adjustments'))), ('Liabilities', (('cl', 'Current Liabilities'), ('ltl', 'Long Term Liabilities'))), ('Equity', (('cap', 'Capital'), ('cadj', 'Capital Adjustments'), ('in', 'Income'), ('ex', 'Expense'))), ('Other', (('excl', 'Excluded'),))], max_length=10, verbose_name='Account Role')),
                ('balance_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=6, verbose_name='Account Balance Type')),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('active', models.BooleanField(default=False, verbose_name='Active')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
            },
        ),
        migrations.CreateModel(
            name='ChartOfAccountModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='CoA Description')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Chart of Account',
                'verbose_name_plural': 'Chart of Accounts',
            },
        ),
        migrations.CreateModel(
            name='EntityManagementModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('permission_level', models.CharField(choices=[('read', 'Read Permissions'), ('write', 'Read/Write Permissions'), ('suspended', 'No Permissions')], default='read', max_length=10, verbose_name='Permission Level')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EntityModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='admin_of', to=settings.AUTH_USER_MODEL, verbose_name='Admin')),
                ('coa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='entity', to='django_ledger.ChartOfAccountModel', verbose_name='Chart of Accounts')),
                ('managers', models.ManyToManyField(related_name='managed_by', through='django_ledger.EntityManagementModel', to=settings.AUTH_USER_MODEL, verbose_name='Managers')),
            ],
            options={
                'verbose_name': 'Entity',
                'verbose_name_plural': 'Entities',
            },
            bases=(models.Model, django_ledger.models.mixins.io.IOMixIn),
        ),
        migrations.CreateModel(
            name='JournalEntryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('date', models.DateField(verbose_name='Date')),
                ('description', models.CharField(blank=True, max_length=70, null=True, verbose_name='Description')),
                ('activity', models.CharField(choices=[('op', 'Operating'), ('fin', 'Financing'), ('inv', 'Investing'), ('other', 'Other')], max_length=5, verbose_name='Activity')),
                ('origin', models.CharField(blank=True, max_length=30, null=True, verbose_name='Origin')),
            ],
            options={
                'verbose_name': 'Journal Entry',
                'verbose_name_plural': 'Journal Entries',
            },
        ),
        migrations.CreateModel(
            name='TransactionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('tx_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=10, verbose_name='Tx Type')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tx Description')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='txs', to='django_ledger.AccountModel', verbose_name='Account')),
                ('journal_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='txs', to='django_ledger.JournalEntryModel', verbose_name='Journal Entry')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='LedgerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('posted', models.BooleanField(default=False, verbose_name='Posted')),
                ('locked', models.BooleanField(default=False, verbose_name='Locked')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledgers', to='django_ledger.EntityModel', verbose_name='Entity')),
            ],
            options={
                'verbose_name': 'Ledger',
                'verbose_name_plural': 'Ledgers',
            },
            bases=(models.Model, django_ledger.models.mixins.io.IOMixIn),
        ),
        migrations.AddField(
            model_name='journalentrymodel',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entry', to='django_ledger.LedgerModel', verbose_name='Ledger'),
        ),
        migrations.AddField(
            model_name='journalentrymodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.JournalEntryModel', verbose_name='Parent'),
        ),
        migrations.AddField(
            model_name='entitymanagementmodel',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_permissions', to='django_ledger.EntityModel', verbose_name='Entity'),
        ),
        migrations.AddField(
            model_name='entitymanagementmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_permissions', to=settings.AUTH_USER_MODEL, verbose_name='Manager'),
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='coa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='django_ledger.ChartOfAccountModel', verbose_name='Chart of Accounts'),
        ),
        migrations.AddField(
            model_name='accountmodel',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='django_ledger.AccountModel', verbose_name='Parent'),
        ),
        migrations.AlterUniqueTogether(
            name='accountmodel',
            unique_together={('coa', 'code')},
        ),
    ]
