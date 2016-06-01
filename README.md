# django-reports

A reports tool based on Django.

Based on and learned from:

- https://github.com/sshwsfc/xadmin
- https://github.com/almasaeed2010/AdminLTE
- https://github.com/frmdstryr/django-xadminlte
- Django 1.9
- https://github.com/maraujop/django-crispy-forms
- https://github.com/zzzeek/sqlalchemy


# Installation
## Install  Requires 
1. Install base requirements

    pip install -r requirements.txt
    
2. Install xadminlte
- Copy the xadminlte app to your django project
- Download AdminLTE and extract it to 'static/xadminlte' (or update the links in base.html)
- Include 'xadminlte' in your installed apps before 'xadmin'

## Install django-reports
- Copy the reports app to your django project
- Include 'reports' in your installed apps
- Include 'reports.urls' in your urls.py