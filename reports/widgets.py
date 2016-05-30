#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dalin at 16-5-21
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.forms.utils import flatatt
from django.utils.encoding import force_unicode, smart_unicode
from xadmin.util import vendor
import logging
logger = logging.getLogger('django.request')


class SliceTypeSelect(forms.Widget):

    def __init__(self, slices, attrs=None):
        super(SliceTypeSelect, self).__init__(attrs)
        self._slices = slices

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['class'] = 'nav nav-pills nav-stacked'
        output = [u'<ul%s>' % flatatt(final_attrs)]
        options = self.render_options(force_unicode(value), final_attrs['id'])
        if options:
            output.append(options)
        output.append(u'</ul>')
        output.append('<input type="hidden" id="%s_input" name="%s" value="%s"/>' %
                     (final_attrs['id'], name, force_unicode(value)))
        return mark_safe(u'\n'.join(output))

    def render_option(self, selected_choice, slice, id):
        if slice.slice_type == selected_choice:
            selected_html = u' class="active"'
        else:
            selected_html = ''
        return (u'<li%s><a onclick="' +
                'javascript:$(this).parent().parent().find(\'>li\').removeClass(\'active\');$(this).parent().addClass(\'active\');' +
                '$(\'#%s_input\').attr(\'value\', \'%s\')' % (id, slice.slice_type) +
                '"><h4><i class="%s"></i> %s</h4><p>%s</p></a></li>') % (
                    selected_html,
                    slice.slice_icon,
                    slice.slice_title or slice.slice_type,
                    slice.description)

    def render_options(self, selected_choice, id):
        # Normalize to strings.
        output = []
        for slice in self._slices:
            output.append(self.render_option(selected_choice, slice, id))
        return u'\n'.join(output)


class SerieEditWidget(forms.Widget):

    def __init__(self, attrs=None):
        super(SerieEditWidget,self).__init__(attrs)
        self.fields = (
            ('type', _('Index way of data column')),
            ('value', _('Data column')),
            ('name', _('Data Name'))
        )
        self.TYPE_CHOICE = (
            ('column_name', _('column name')),
            ('column_index', _('column index'))
        )

    @property
    def media(self):
        return vendor('sliceedit.js',)

    def render(self, name, value, attrs=None):
        logger.debug('render value: %s' % value)
        if value is None:
            value = ''

        if not isinstance(value, dict):
            value = self.decompress(value)
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs['class'] = 'form-inline'
        output = [u'<div%s>' % flatatt(final_attrs)]
        options = self.render_options(final_attrs['id'], name, value)
        if options:
            output.append(options)
        output.append('<span class="btn btn-primary btn-small btn-ajax pull-right" title="%s" onclick="' % _('Add a new serie') +
                      'javascript:$(this).parent().parent().append($(this).parent().clone(true))' +
                      '"><i class="fa fa-plus"></i></span>')
        output.append('<span class="btn btn-primary btn-small btn-ajax pull-right" title="%s" onclick="' % _('Remove this serie') +
                      'javascript:$(this).parent().remove()' +
                      '"><i class="fa fa-minus"></i></span>')
        output.append('</div>')
        return mark_safe(u'\n'.join(output))

    def render_option(self, field, id, name, value):
        id = '%s-%s' %(id, field[0])
        name = '%s-%s' %(name, field[0])
        output = ['<div class="form-group">',]
        output.append('<label for="%s">%s</label>' % (id, field[1]))
        logger.debug('reder_option value: %s' % value)
        if isinstance(value, dict) and field[0] in value.keys():
            option_value = value[field[0]][0]
        else:
            option_value = None
        if field[0] == 'type':
            output.append(
                forms.Select(choices=self.TYPE_CHOICE).render(name=name, value=option_value,
                                                              attrs={'id': id, 'class':'select form-control', 'style': 'min-width:60px'}))
        else:
            output.append(forms.TextInput().render(name=name, value=option_value, attrs={'id': id, 'class': 'textInput form-control'}))
        output.append('</div>')

        return mark_safe(u'\n'.join(output))

    def render_options(self, id, name, value):
        output = []
        logger.debug('reder_options value: %s' % value)
        for field in self.fields:
            output.append(self.render_option(field, id, name, value))
        return u'\n'.join(output)

    def value_from_datadict(self, data, files, name):
        logger.debug('value_from_datadict: data:%s, files:%s, name:%s' % (data, files, name))
        adata = dict(data.iterlists())
        temp_data = {}
        for k, v in adata.items():
            if name+'-' in k:
                key = k.split('-')[-1]
                temp_data[key] = v
                logger.debug('key: %s, data[key]: %s' % (k, v))
                #del data[k]

        logger.debug('new data: %s' %temp_data)
        data[name] = temp_data
        logger.debug('value_from_datadict after: data:%s, files:%s, name:%s' % (data, files, name))
        return temp_data

    def decompress(self, value):
        logger.debug('decompress value: %s' % value)
        if value:
            return [v for k, v in value]
        return ['', '', '']
