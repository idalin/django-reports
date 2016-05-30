#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dalin at 16-5-23
from django import forms
from django.utils.translation import ugettext as _
from xadmin import widgets as exwidgets
from django.core import validators
from django.core.exceptions import ValidationError
import logging
from reports.widgets import SerieEditWidget
logger = logging.getLogger('django.request')



INDEX_WAY = (
    ('column_name',_('column name')),
    ('column_index', _('column index'))
)


AXIS_TYPE = (
    ('value', _('value')),
    ('category', _('category')),
    ('time', _('time')),
    ('log', _('log')),
)


class LineEditWidget(forms.MultiWidget):
    def __init__(self,*args,**kwargs):
        widgets = (
            forms.Select(choices=INDEX_WAY),
            forms.TextInput(),
            forms.TextInput(),
        )
        super(LineEditWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        logger.debug('decompress value: %s' % value)
        if value:
            return [v for k, v in value]
        return ['', '', '']


class LineField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        fields = (
            forms.ChoiceField(),
            forms.CharField(),
            forms.CharField()
        )
        super(LineField, self).__init__(fields, *args, **kwargs)
        self.widget = SerieEditWidget(attrs={'class': 'form-inline'})

    def compress(self, data_list):
        logger.debug('compress data_list: %s' % data_list)
        series = []
        if data_list and isinstance(data_list, dict):
            for k, v in data_list.items():
                for i, real_v in enumerate(v):
                    if len(series) < i+1:
                        series.append({})
                    if k == 'name':
                        series[i]['name'] = real_v
                    else:
                        if 'data' not in series[i].keys():
                            series[i]['data'] = {}
                        series[i]['data'][k] = real_v
            logger.debug('compressed data: %s' % series)
            return series
        return None

    def clean(self, value):
        clean_data = {}
        errors = []
        logger.debug('cleaning myself! %s' % value)
        if not value or isinstance(value, (list, tuple, dict)):
            if not value or not [v for v in value if v not in self.empty_values]:
                if self.required:
                    raise ValidationError(self.error_messages['required'], code='required')
                else:
                    return self.compress([])
        else:
            raise ValidationError(self.error_messages['invalid'], code='invalid')

        if isinstance(value, dict):
            for k, v in value.items():
                if k not in clean_data.keys():
                    clean_data[k] = []
                if k == 'type':
                    for v1 in v:
                        clean_data[k].append(forms.ChoiceField(choices=INDEX_WAY).clean(v1))
                else:
                    for v1 in v:
                        clean_data[k].append(forms.CharField().clean(v1))
        logger.debug('clean data: %s' % value)
        #new_value = [f[1] for f in value]
        #clean_data = super(LineField, self).clean(new_value)
        logger.debug('clean data:%s' % clean_data)
        out = self.compress(clean_data)
        return out


class AxisEditField(forms.MultiValueField):

    def __init__(self, *args, **kwargs):
        pass



class SliceManager(object):
    _slices = None

    def __init__(self):
        self._slices = {}

    def register(self, slice_class):
        self._slices[slice_class.slice_type] = slice_class
        return slice_class

    def get(self, name):
        return self._slices[name]

    def get_slices(self):
        return self._slices.values()

slice_manager = SliceManager()


class BaseSlice(forms.Form):

    template = 'xadmin/slices/base.html'
    description = 'Base Slice, don\'t use it.'
    slice_title = None
    slice_icon = 'fa fa-plus-square'
    slice_type = 'base'
    base_title = None

    id = forms.IntegerField(label=_('Slice ID'), widget=forms.HiddenInput)
    title = forms.CharField(label=_('Slice Title'), required=False, widget=exwidgets.AdminTextInputWidget)


@slice_manager.register
class TableSlice(BaseSlice):
    slice_type = 'table'
    slice_icon = 'fa fa-table'
    description = _('Data Grids(Table)')
    slice_title = _('Table')


class EchartsBaseSlice(BaseSlice):
    #chart title options
    title_show = forms.BooleanField(label=_('Show Title?'), initial=False, required=False)

    #legend options
    legend_show = forms.BooleanField(label=_('Show legend?'), initial=True, required=False)

    #tooltip options
    tooltip_show = forms.BooleanField(label=_('Show tooltip?'), initial=True, required=False)

    #toolbox options
    toolbox_show = forms.BooleanField(label=_('Show toolbox?'), initial=True, required=False)


class GridBaseSlice(EchartsBaseSlice):
    #grid options
    grid_show = forms.BooleanField(label=_('Show grid?'), initial=False, required=False)

    #xAxis options
    xAxis_type = forms.ChoiceField(
        label=_('X Axis Type'),
        choices=AXIS_TYPE,
        initial='category',
        help_text=_("""
        'value' 数值轴，适用于连续数据。
        'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。
        'time' 时间轴，适用于连续的时序数据，与数值轴相比时间轴带有时间的格式化，在刻度计算上也有所不同，例如会根据跨度的范围来决定使用月，星期，日还是小时范围的刻度。
        'log' 对数轴。适用于对数数据。
        """)
    )
    xAxis = LineField(label=_('xAxis'))
    yAxis_type = forms.ChoiceField(
        label=_('Y Axis Type'),
        choices=AXIS_TYPE,
        initial='value',
        help_text=_("""
        'value' 数值轴，适用于连续数据。
        'category' 类目轴，适用于离散的类目数据，为该类型时必须通过 data 设置类目数据。
        'time' 时间轴，适用于连续的时序数据，与数值轴相比时间轴带有时间的格式化，在刻度计算上也有所不同，例如会根据跨度的范围来决定使用月，星期，日还是小时范围的刻度。
        'log' 对数轴。适用于对数数据。
        """)
    )
    series = LineField()



@slice_manager.register
class LineSlice(GridBaseSlice):
    slice_type = 'line'
    slice_icon = 'fa fa-line-chart'
    description = _('Echarts Line chart')
    slice_title = _('Line')
    #series = forms.CharField(label=_('Line config'), max_length=256, widget=SerieEditWidget)


@slice_manager.register
class BarSlice(GridBaseSlice):
    slice_type = 'bar'
    slice_icon = 'fa fa-bar-chart'
    description = _('Echarts Bar chart')
    slice_title = _('Bar')


@slice_manager.register
class PieSlice(EchartsBaseSlice):
    slice_type = 'pie'
    slice_icon = 'fa fa-pie-chart'
    description = _('Echarts Pie chart')
    slice_title = _('Pie')


@slice_manager.register
class MapSlice(EchartsBaseSlice):
    slice_type = 'map'
    slice_icon = 'fa fa-map'
    description = _('Echarts Map chart')
    slice_title = _('Map')


@slice_manager.register
class RadarSlice(EchartsBaseSlice):
    slice_type = 'radar'
    slice_icon = 'fa fa-star'
    description = _('Echarts Radar chart')
    slice_title = _('Radar')


@slice_manager.register
class CustomSlice(BaseSlice):
    slice_type = 'custom'
    slice_icon = 'fa fa-wrench'
    description = _('Custom your own chart')
    slice_title = _('Custom Chart')
