#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A pointer marker management class.
"""

import jinja2

from . import double_gis_util
from . import marker_icon

from iq.util import log_func

__version__ = (0, 0, 0, 1)


MARKER_TEMPLATE = '''
DG.marker({{ location }}{% if icon %}, {icon: DG.icon({iconUrl: '{{ icon }}', iconSize: [32, 32], iconAnchor: [16, 31]})}{% endif %}).addTo(map)
{% if tooltip %}.bindLabel('{{ tooltip }}'){% endif %}
{% if popup %}.bindPopup('{{ popup }}'){% endif %}
;
'''


class iq2GISMarker(object):
    """
    Pin marker.
    """
    _marker_template = jinja2.Template(MARKER_TEMPLATE)

    def __init__(self, location,
                 popup=None, tooltip=None,
                 icon=None,
                 **kwargs):
        """
        Constructor.

        :param location: Marker geolocation.
        :param popup: Marker pop-up text.
            A tooltip appears by clicking on the marker.
        :param tooltip: Marker pop-up text.
            A tooltip appears when you hover the mouse over the marker.
        :param icon: Icon.
        """
        if location is None:
            # If location is not passed we center and zoom out.
            self.location = [0, 0]
        else:
            self.location = double_gis_util.validate_location(location)

        self.popup = popup
        self.tooltip = tooltip

        self.icon = marker_icon.get_marker_icon_filename(icon)

    def render(self, **kwargs):
        """
        Generates the HTML representation of the element.

        :return: The generated HTML representation of the map.
        """
        return self._marker_template.render(location=self.location,
                                            icon=self.icon,
                                            popup=self.popup,
                                            tooltip=self.tooltip,
                                            **kwargs)

    def add_to(self, geo_map):
        """
        Add a marker to the map.

        :param geo_map: Map object.
        :return: True/False.
        """
        try:
            geo_map.add_marker(self)
            return True
        except:
            log_func.fatal(u'Error adding pointer marker to map')
        return False


# To support rendering, class names need to be overridden
Marker = iq2GISMarker
