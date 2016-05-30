#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dalin at 16-5-18
from django import forms
from django.utils.translation import ugettext as _
from django.forms.forms import DeclarativeFieldsMetaclass
import xadmin
from xadmin.views import DetailAdminView
from reports.models import Slice, DataSource, Filter, SQL
from reports.views import SliceView
from reports.widgets import SliceTypeSelect
from reports.slice import slice_manager
from . import vendors
import copy
import logging

logger = logging.getLogger('django.request')


class GlobalSetting(object):
    menu_style = 'default'
    site_title = u'django-reports'
    site_footer = u'django-reports'
xadmin.site.register(xadmin.views.CommAdminView, GlobalSetting)


class SliceAdmin(object):
    detail_template = 'reports/views/slice.html'
    exclude = ['id']
    wizard_form_list = (
        (_('Slice base info and data configurations'), ('name', 'description', 'sql')),
        (_('Slice Type'), ('slice_type',)),
        (_('Slice display configurations'), {'callback': 'get_slice_params_form', 'convert': 'convert_slice_params'})
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'slice_type':
            slices = slice_manager.get_slices()
            form_widget = SliceTypeSelect(slices)
            return forms.ChoiceField(choices=[(s.slice_type, s.description) for s in slices],
                                     widget=form_widget, label=_('Slice Type'))
        field = super(
            SliceAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        return field

    def get_slice_params_form(self, wizard):
        data = wizard.get_cleaned_data_for_step(wizard.steps.prev)
        slice_type = data['slice_type']
        slice = slice_manager.get(slice_type)
        fields = copy.deepcopy(slice.base_fields)
        if 'id' in fields:
            del fields['id']
        if 'title' in fields:
            del fields['title']
        logger.debug(fields)
        return DeclarativeFieldsMetaclass("SliceParamsForm", (forms.Form,), fields)

    def convert_slice_params(self, wizard, cleaned_data, form):
        slice = Slice()
        value = dict([(f.name, f.value()) for f in form])
        logger.debug('Value before: %s' % value)
        params = {}
        columns = {}
        if value['title_show']:
            params['title'] = {'text': cleaned_data['name']}
        if value['tooltip_show']:
            params['tooltip'] = {'trigger': 'axis'}
        if value['toolbox_show']:
            params['toolbox'] = {'show': True}
        if value['legend_show']:
            params['legend'] = {'show': True}
        if value['grid_show']:
            params['grid'] = {'show': True}
        for key in value.keys():
            if key.endswith('_show'):
                del value[key]
                continue
            if key.lower() == 'series' or key.lower() == 'xaxis':
                params[key] = self.convert_series(value[key])
                del value[key]
                continue
                logger.debug('params[key] %s' % params[key])

        if 'xAxis_type' in value.keys() and 'xaxis' in params.keys():
            params['xaxis']['type'] = value['xAxis_type']
            del value['xAxis_type']

        for serie in params['series']:
            serie['type'] = 'line'
        params.update(value)
        logger.debug('Value after: %s' % params)
        slice.set_params(params)
        cleaned_data['params'] = slice.params

    def convert_series(self, series):
        new_series = []
        for k, v in series.items():
            for i, real_v in enumerate(v):
                if len(new_series) < i+1:
                    new_series.append({})
                if k == 'name':
                    new_series[i]['name'] = real_v
                else:
                    if 'data' not in new_series[i].keys():
                        new_series[i]['data'] = {}
                    new_series[i]['data'][k] = real_v
        logger.debug('new series:%s' % new_series)
        return new_series

class DataSourceAdmin(object):
    exclude = ['id']


class FilterAdmin(object):
    pass


class SQLAdmin(object):
    pass

xadmin.site.register(Slice, SliceAdmin)
xadmin.site.register(DataSource, DataSourceAdmin)
xadmin.site.register(SQL, SQLAdmin)
xadmin.site.register(Filter, FilterAdmin)
xadmin.site.register_modelview(r'^(.+)$', SliceView, name='%s_%s_slice')
