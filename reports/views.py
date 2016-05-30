#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import decimal, datetime
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, View
from django import forms
from django.template import loader
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.utils.encoding import force_unicode, smart_unicode
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import DeclarativeMeta
from xadmin.sites import site
from xadmin import widgets
from xadmin.views import DetailAdminView, BaseAdminPlugin, UpdateAdminView
import json
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Fieldset,Field
from reports.models import DataSource, Slice
# Create your views here.
ERROR_FLAG = 'e'

logger = logging.getLogger('django.request')


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


class FilterForm(forms.Form):
    def __init__(self, filters, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        logger.debug('args:%s, kwargs: %s' % (args, kwargs))
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal form-inline exform'
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'
        self.helper.form_method = 'GET'
        self.helper.form_action = ''
        for f in filters:
            name = f['name']
            if name in args[0].keys():
                default_value = args[0][name]
            else:
                default_value = f['default_value']
            f_type = f['type']
            description = f['description']
            logger.debug('initial: %s' % default_value)
            if f_type == 'Date':
                self.fields[name] = forms.DateField(label=description, widget=widgets.AdminDateWidget, required=False, initial=default_value)
            else:
                self.fields[name] = forms.CharField(initial=default_value, label=description, widget=widgets.AdminTextInputWidget, required=False)
        self.helper.layout = Layout(
            Submit(_('Submit'), _('Submit'), css_class='pull-right')
        )
        self.helper.layout.extend(map(lambda f: Field(f), self.fields))
        #logger.debug(self.helper.layout)


    def media(self):
        return forms.Media()


class SliceView(DetailAdminView):
    detail_template = 'reports/views/slice.html'
    filter_template = None
    slice_template = None
    show_filters = True

    def get_filter(self):
        return self.obj.sql.filters.all().values()

    def get_filter_form(self):
        f = self.get_filter()
        return FilterForm(f, dict(self.request.GET.items()))

    def get_slice(self):
        logger.debug('starting to load params')
        params = json.loads(self.obj.params)
        self.data = self.get_data()
        for k, v in params.iteritems():
            logger.debug('key: %s, value: %s'%(k,v))
            if k.lower() in ('series', 'xaxis'):
                if isinstance(v, list):
                    for s in v:
                        s['data'] = self.convert_data(s['data'])
                elif isinstance(v, dict):
                    v['data'] = self.convert_data(v['data'])

        return params

    def convert_data(self, data_obj):
        if not isinstance(data_obj, dict):
            return None
        if data_obj['type'] == 'column_index':
            logger.debug('data_obj[value]: %s' % data_obj['value'])
            cindex = int(data_obj['value'])
        else:
            cindex = data_obj['value']

        return [unicode(r[cindex]) for r in self.data]

    def get(self, request, *args, **kwargs):
        form = self.get_model_form()
        self.form_obj = form(instance=self.obj)
        helper = self.get_form_helper()
        format = self.request.GET.get('format', None)
        if helper:
            self.form_obj.helper = helper
        if request.is_ajax() or format == 'json':
            return self.get_jsonresponse()
        elif format == 'raw':
            res = [dict(r) for r in self.get_data()]
            return JsonResponse(json.dumps(res, default=alchemyencoder), safe=False)
        else:
            if format == 'print':
                self.base_template = 'xadmin/base.html'
            return self.get_response()

    def get_jsonresponse(self):
        self.get_slice()
        return JsonResponse(self.get_slice())

    def get_data(self, **kwargs):
        from sqlalchemy import create_engine
        datasource = self.obj.sql.datasource
        db_str = str('%s://%s:%s@%s:%s/%s' % (
            datasource.type.lower(),
            datasource.username,
            datasource.password,
            datasource.host,
            datasource.port,
            datasource.db_name
        ))
        engine = create_engine(db_str)
        logger.debug('database: %s' % db_str)
        sql = self.get_sql()
        conn = engine.connect()
        result = conn.execute(sql).fetchall()
        logger.debug(result[0][1])
        return result

    def get_context(self):
        context = super(SliceView, self).get_context()
        data = self.get_data()
        new_context = {
            'title': self.obj.name,
            'filters': self.get_filter(),
            'form': self.get_filter_form(),
            'data': data,
            'slice': self.obj,
            'slice_url': self.get_slice_url(self.obj.pk),
            'base_template': self.base_template
        }
        context.update(new_context)
        return context

    def get_media(self):
        media = super(SliceView, self).get_media()
        media.add_js(['reports/js/slice.js', 'reports/vendor/echarts/echarts.js','reports/vendor/echarts/shine.js'])
        return media + self.vendor('datepicker.js', 'datepicker.css', 'xadmin.widget.datetime.js')

    def get_sql(self):
        p = dict(self.request.GET.items()).copy()
        filters = self.get_filter()
        filter_names = map(lambda n: n['name'], filters)
        for k in p.keys():
            if k not in filter_names:
                del p[k]
        sql = text(self.obj.sql.value)
        params = {}
        for f in filters:
            if f['name'] in p.keys() and p[f['name']]:
                params[f['name']] = p[f['name']]
            else:
                params[f['name']] = f['default_value']
        sql = sql.bindparams(**params)
        logger.debug(p)
        logger.debug('raw sql: %s' % sql)
        logger.debug(params)
        return sql

    def get_response(self, *args, **kwargs):
        context = self.get_context()
        context.update(kwargs or {})
        logger.debug('query string: %s' % self.request.GET.values())
        return TemplateResponse(self.request, self.detail_template or
                                self.get_template_list(
                                    'views/model_detail.html'),
                                context, current_app=self.admin_site.name)

    def get_slice_url(self, sid):
        return self.model_admin_url('slice', sid) + self.get_query_string()

    def block_filters(self, context, nodes):
        context['filter_title'] = _('Filters')
        #logger.debug(self.get_filter_form())
        nodes.append(loader.render_to_string(self.filter_template or 'reports/includes/filters.html', context_instance=context))

    def block_slice(self, context, nodes):
        context['slice_title'] = self.obj.name
        nodes.append(loader.render_to_string(self.slice_template or 'reports/includes/slice.html', context_instance=context))


