#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by dalin at 16-5-9
from xadmin import vendors

vendors.vendors.update({
    "bootstrap": {
        'js': {
            'dev': 'reports/vendor/bootstrap/js/bootstrap.js',
            'production': 'reports/vendor/bootstrap/js/bootstrap.min.js',
            'cdn': 'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/js/bootstrap.min.js'
        },
        'css': {
            'dev': 'reports/vendor/bootstrap/css/bootstrap.css',
            'production': 'reports/vendor/bootstrap/css/bootstrap.css',
            'cdn': 'http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.1/css/bootstrap-combined.min.css'
        },
        'responsive': {'css': {
            'dev': 'reports/vendor/bootstrap/bootstrap-responsive.css',
            'production': 'reports/vendor/bootstrap/bootstrap-responsive.css'
        }}
    },
    "AdminLTE": {
        "js": {
            "dev": "reports/vendor/AdminLTE/js/app.js",
            "production": "reports/vendor/AdminLTE/js/app.min.js",
        },
        "css": {
            "dev": "reports/vendor/AdminLTE/css/AdminLTE.css",
            "production": "reports/vendor/AdminLTE/css/AdminLTE.min.css",
        }
    },
    'jquery': {
        "js": {
            'dev': 'reports/vendor/jquery/jquery.js',
            'production': 'reports/vendor/jquery/jquery.min.js',
        }
    },
    'echarts': {
        "js": {
            'dev': 'reports/vendor/echarts/echarts.js',
            'production': 'reports/vendor/echarts/echarts.min.js',
        }
    },
    "font-awesome": {
        "css": {
            'dev': 'reports/vendor/font-awesome/css/font-awesome.css',
            'production': 'reports/vendor/font-awesome/css/font-awesome.min.css',
        }
    },
    "sliceedit":{
        "js":{
            "dev": "reports/js/sliceedit.js",
            "production": "reports/js/sliceedit.js",
        }
    }
})
