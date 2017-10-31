from __future__ import unicode_literals

import json

from django import forms
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from .conf import settings


class GeopositionWidget(forms.MultiWidget):
    template_name = 'geoposition/widgets/geoposition.html'

    def __init__(self, attrs=None):
        widgets = (
            forms.TextInput(),
            forms.TextInput(),
        )
        super(GeopositionWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, six.text_type):
            return value.rsplit(',')
        if value:
            return [value.latitude, value.longitude]
        return [None, None]

    def get_config(self):
        return {
            'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
            'map_options': json.dumps(settings.MAP_OPTIONS),
            'marker_options': json.dumps(settings.MARKER_OPTIONS),
        }


    def get_context(self, name, value, attrs):
        # Django 1.11 and up
        ctx = super(GeopositionWidget, self).get_context(name, value, attrs)
        ctx['config'] = {
            'map_widget_height': settings.MAP_WIDGET_HEIGHT or 500,
            'map_options': json.dumps(settings.MAP_OPTIONS),
            'marker_options': json.dumps(settings.MARKER_OPTIONS),
        }

        ctx['latitude'] = {
            'html': ctx['widget']['subwidgets'][0],
            'label': _("latitude"),
        }
        ctx['longitude'] = {
            'html': ctx['widget']['subwidgets'][1],
            'label': _("longitude"),
        }
        return ctx

    class Media:
        js = (
            '//maps.google.com/maps/api/js?key=%s' % settings.GOOGLE_MAPS_API_KEY,
            'geoposition/geoposition.js',
        )
        css = {
            'all': ('geoposition/geoposition.css',)
        }
