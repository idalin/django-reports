from django.utils.translation import ugettext as _
from django.db import models
#from jsonfield2 import JSONField, JSONAwareManager
import json
from  xadmin.models import JSONEncoder
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username_field = User.USERNAME_FIELD
except Exception:
    from django.contrib.auth.models import User
    username_field = 'username'
import logging

logger = logging.getLogger('django.request')


DATASOURCE_TYPE = (
    ('MySQL', 'MySQL'),
    ('SQLite', 'SQLite3'),
    ('Oracle', 'Oracle'),
    ('MSSQL', 'MicroSoft SQLServer'),
)


SLICE_TYPE = (
    ('Table', _('Table')),
    ('Line', _('Line')),
    ('Bar', _('Bar')),
    ('Map', _('Map')),
    ('Pie', _('Pie')),
    ('Radar', _('Radar')),
    ('Custom', _('Custom Slice')),
)


class DataSource(models.Model):
    name = models.CharField(_('DataSource Name'), max_length=128)
    type = models.CharField(_('DataSource Type'), max_length=32, choices=DATASOURCE_TYPE, default='MySQL')
    host = models.CharField(_('Host IP'), default='127.0.0.1', max_length=128)
    port = models.IntegerField(_('DataBase Port'), default=3306)
    db_name = models.CharField(_('DataBase Name'), max_length=128)
    username = models.CharField(_('DataBase Username'), max_length=128, default='root')
    password = models.CharField(_('DataBase Password'), max_length=128)

    def __unicode__(self):
        return u'%s' % self.name


class Report(models.Model):
    owner = models.ForeignKey(User, null=True)


class Filter(models.Model):
    FILTERTYPE = (
        ('Date', _('Date')),
        ('Text', _('Text')),
        ('Select', _('Select')),
        ('Month', _('Month')),
        ('SRCSelect', _('Select from a source')),
        ('HLDSelect', _('Select from a source')),
    )
    #slice = models.ForeignKey(Slice)
    name = models.CharField(_('Filter Name'), max_length=128)
    type = models.CharField(_('Filter Type'), max_length=64, choices=FILTERTYPE)
    description = models.CharField(_('Description of This Filter'), max_length=128)
    default_value = models.CharField(_('Default Value of this filter'), max_length=256, blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.description


class SQL(models.Model):
    filters = models.ManyToManyField(Filter)
    datasource = models.ForeignKey(DataSource)
    description = models.CharField(_('Description'), max_length=256, blank=True, null=True)
    value = models.TextField(_('SQL statements'), max_length=2048, default='Null')

    def __unicode__(self):
        return u'%s' % self.description


class Slice(models.Model):
    sql = models.ForeignKey(SQL)
    slice_type = models.CharField(_('Slice Type'), max_length=64, default='line')
    name = models.CharField(_('Title Of Slice'), max_length=256, null=True, blank=True)
    params = models.TextField(_('Slice Parameters'))
    description = models.CharField(_('Description of This Slice'), max_length=128, null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.description

    def get_data(self, **kwargs):
        pass

    def set_params(self, obj):
        logger.debug('object: %s' % obj)
        self.params = json.dumps(obj, cls=JSONEncoder, ensure_ascii=False)
        logger.debug('params: %s' % self.params)

    def connect_db(self):
        pass

    def get_filters(self):
        return self.filters.all()

